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


    #CONSTRUCTOR
    def __init__(self,name=None,*args,**kwargs):
        self.REDIRECT_TYPE = type(render_to_string(self.REDIRECT_TEMPLATE_PATH,{}))
        View.__init__(self,*args,**kwargs)
        self.name = self.getName(name)

    def getName(self,name):
        if name != None:
            name = self.NAME+"_"+str(name)
        else:
            name = self.NAME
        return name


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
    def render(self,handle=False,**kwargs):
        """
        Callable function that returns the page's html
        """

        #Check name
        if self.NAME == None:
            raise Exception("must define self.NAME")

        #Check auth
        if self.AUTH_REQUIRED and \
           not self.checkAuth(**kwargs):
            return self.redirect(args={page:"authentication"},**kwargs)

        #Check for delete
        if "delete_"+self.NAME in kwargs:
            delete_result = self.delete(**kwargs)
            if type(delete_result) == self.REDIRECT_TYPE:
                return delete_result

        #Check for save
        if "save_"+self.NAME in kwargs:
            save_result = self.save(**kwargs)
            if type(save_result) == self.REDIRECT_TYPE:
                return save_result

        #Get context
        context = self.fetch(**kwargs)
        #Check for redirect
        if type(context) == self.REDIRECT_TYPE:
            return context

        if type(context) != type({}):
            raise Exception("context must be a {} type")
        part_dict = self.renderParts(kwargs)
        for part_name in part_dict:
            context[part_name] = part_dict[part_name]
        #Add self to context
        context["self"] = self

        if self.TEMPLATE_PATH == None:
            raise Exception("must define a self.TEMPLATE_PATH")
        request = kwargs["request"]
        context_instance = RequestContext(request,context)
        html = render_to_string(self.TEMPLATE_PATH,context,context_instance)

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
                        "id": self.name+"_container",
                        "content": html,
                    }
            context_instance = RequestContext(request,context)
            html = render_to_string(self.CONTAINER_TEMPLATE_PATH,context,context_instance)

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
            part_dict[part.name] = part.render(**kwargs)
        return part_dict

    def checkAuth(self,request,**kwargs):
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
        context_instance = RequestContext(request,context)
        redirect = render_to_string(self.REDIRECT_TEMPLATE_PATH,
                                    context,
                                    context_instance)
        return redirect


    #OVERRIDE METHODS
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
