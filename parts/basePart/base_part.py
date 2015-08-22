from django.views.generic import View
from django.http import HttpResponse
from django.template import RequestContext
from django.template.loader import render_to_string


class BasePart(View):
    NAME = None
    TEMPLATE_PATH = None
    PART_LIST = []
    RENDER_PART_LIST = False
    CONTAINER_TEMPLATE_PATH = "parts/container.html"
    AUTH_REQUIRED = False
    REDIRECT_TEMPLATE_PATH = "parts/redirect.html"
    CONTENT_VARIABLE = None
    CONTENT_DEFAULT = None
    CLASS = None

    #CONSTRUCTOR
    def __init__(self,prefix=None,*args,**kwargs):
        self.REDIRECT_TYPE = type(render_to_string(self.REDIRECT_TEMPLATE_PATH,{}))
        self.HTTP_RESPONSE_TYPE = type(HttpResponse())
        View.__init__(self,*args,**kwargs)
        self.prefix = prefix
        self.setName(self.prefix)

    def setName(self,prefix):
        if prefix != None:
            name = str(prefix) +"__"+ self.NAME
        else:
            name = self.NAME
        self.name = name
        self.container = name+"__container"


    #WEB METHODS
    def get(self,request,*args,**kwargs):
        return self.handle(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        return self.handle(request,*args,**kwargs)

    def handle(self,request,*args,**kwargs):
        """
        A common function to handle both get and post requests
        """
        kwargs = self.makeArgs(request,kwargs)
        html = self.render(handle=True,**kwargs)
        return HttpResponse(html)

    def makeArgs(self,request,kwargs):
        if hasattr(request,"FILE"):
            file_dict = request.FILE
        else:
            file_dict = {}
        file_dict = self.mergeArgDict({},file_dict)
        post_dict = self.mergeArgDict({},request.POST)
        #Merge file and post dicts
        #Post dict overrides file
        request_args = self.mergeArgDict(file_dict,post_dict,True)
        get_dict = self.mergeArgDict({},request.GET)
        #Merge request_args and get dicts
        #Get dict overrides request_args
        request_args = self.mergeArgDict(request_args,get_dict,True)
        #Merge args from request into kwargs
        #Kwargs is not overridden
        kwargs = self.mergeArgDict(kwargs,request_args,False)
        #Place request in kwargs
        kwargs["request"] = request
        return kwargs

    def mergeArgDict(self,arg_dict,new_dict,override=False):
        for key in new_dict:
            if key in arg_dict and override == False:
                raise Exception("argument, %s, has already been processed" % key)
            arg_dict[key] = new_dict[key]
        return arg_dict


    #RENDER FUNCTION
    def render(self,part_name=None,handle=False,**kwargs):
        """
        Callable function that returns the page's html
        """

        #Check name
        if self.NAME == None:
            raise Exception("must define self.NAME")

        if part_name != None:
            self.name = part_name
            self.container = self.name+"__container"

        #Check authenticated
        if self.AUTH_REQUIRED and \
           not self.checkAuth(**kwargs):
            return self.redirect(args={"page":"authentication"},**kwargs)

        #Check authorized
        self.authorize(**kwargs)

        context = None

        #Check for delete
        if "delete_"+self.NAME in kwargs:
            delete_result = self.delete(**kwargs)
            if type(delete_result) == self.REDIRECT_TYPE:
                return delete_result
            if type(delete_result) == type({}) and\
               context == None:
                context = delete_result

        #Check for save
        if "save_"+self.NAME in kwargs:
            save_result = self.save(**kwargs)
            if type(save_result) == self.REDIRECT_TYPE:
                return save_result
            if type(save_result) == type({}) and\
               context == None:
                context = save_result

        #Get context
        fetch_result = self.fetch(**kwargs)
        if context == None:
            context = fetch_result
        #Check for redirect
        if type(context) == self.REDIRECT_TYPE:
            return context
        #Check for HttpResponse
        if type(context) == self.HTTP_RESPONSE_TYPE:
            return context

        if type(context) != type({}):
            raise Exception("part, {0}, returned context that was not a dict type".format(self.NAME))
        part_dict = self.renderParts(kwargs)
        for part_name in part_dict:
            context[part_name] = part_dict[part_name]
        if self.CONTENT_VARIABLE:
            context["content"] = self.renderContent(kwargs)
        #Add self to context
        context["self"] = self

        if self.TEMPLATE_PATH == None:
            raise Exception("must define a self.TEMPLATE_PATH")
        request = kwargs["request"]
        html = self.renderToString(self.TEMPLATE_PATH,context,request)

        if not handle:
            """
            If the render function was called by the handle method, then that
            means that the part is being loaded individually. This means that
            there is no need for a container div to be rendered.

            If the render function was not called by the handle method, then
            we also need to render the container div and associated js.
            """
            #Need to add container div
            context = {
                        "id": self.name+"__container",
                        "content": html,
                        "self": self,
                    }
            html = self.renderToString(self.CONTAINER_TEMPLATE_PATH,context,request)

        return html

    def renderToString(self,template_path,context,request=None):
        if request:
            context_instance = RequestContext(request,context)
            html = render_to_string(template_path,context,context_instance)
        else:
            html = render_to_string(template_path,context)
        return html

    def renderParts(self,kwargs):
        """
        Renders parts in self.PART_LIST
        Returns dictionary where keys are part_name and values are html
        """
        if not self.RENDER_PART_LIST:
            return {}

        part_dict = {}
        for part in self.PART_LIST:
            part_dict[part.NAME] = part(prefix=self.name).render(**kwargs)
        return part_dict

    def renderContent(self,kwargs):
        if not self.CONTENT_DEFAULT:
            raise Exception("tried to render a content part without self.CONTENT_DEFAULT")

        content_part = None
        if self.CONTENT_VARIABLE in kwargs:
            content_key = kwargs[self.CONTENT_VARIABLE]
        else:
            content_key = self.CONTENT_DEFAULT
        for part in self.PART_LIST:
            if part.NAME == content_key:
                content_part = part
                break
        if not content_part:
            raise Exception("could not find a content part with %s as self.NAME" % content_key)
        return content_part(prefix=self.name).render(**kwargs)

    def checkAuth(self,request=None,**kwargs):
        if not request:
            raise Exception("no request provided")
        return request.user.is_authenticated()

    def redirect(self,request=None,args={},**kwargs):
        if not request:
            raise Exception("tried to redirect without a request object in kwargs")

        arg_list = ["%s=%s" % (key,args[key]) for key in args]
        arg_string = "&".join(arg_list)
        redirect_url = "/?"+arg_string
        context = {
                    "redirect_url": redirect_url,
                }
        redirect = self.renderToString(self.REDIRECT_TEMPLATE_PATH,context,request)
        return redirect


    #OVERRIDE METHODS
    def authorize(self,**kwargs):
        """
        Can be used to raise exceptions before any of the other methods are called
        """
        return

    def fetch(self,**kwargs):
        """
        Gets data and creates context dict
        Override this function to make the context object
        """
        return {}

    def save(self,**kwargs):
        """
        Automatically called when save_NAME is in args
        Should save relevant information and return None
        """
        return

    def delete(self,**kwargs):
        """
        Automatically called when delete_NAME is in args
        Should delete all relevant objects and return None
        """
        return
