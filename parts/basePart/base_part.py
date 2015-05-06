from django.views.generic import View
from django.http import HttpResponse
from django.template import RequestContext
from django.template.loader import render_to_string
import json


class BasePart(View):
    NAME = None
    TEMPLATE_PATH = None
    PART_LIST = []
    CONTAINER_TEMPLATE_PATH = "parts/container.html"
    AUTH_REQUIRED = False
    AUTH_REDIRECT_TEMPLATE_PATH = "parts/auth_redirect.html"
    REDIRECT_TEMPLATE_PATH = "parts/redirect.html"


    def get(self,request,*args,**kwargs):
        return self.handle(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        return self.handle(request,*args,**kwargs)

    def handle(self,request,*args,**kwargs):
        """
        A common function to handle both get and post requests
        """
        kwargs = self.makeArgs(request,kwargs)
        html = self.render(request,handle=True,**kwargs)
        return HttpResponse(html)

    def makeArgs(self,request,kwargs):
        post_dict = self.mergeArgDict({},request.POST)
        get_dict = self.mergeArgDict({},request.GET)
        #Merge post and get dicts
        #Get dict overrides post
        request_args = self.mergeArgDict(post_dict,get_dict,True)
        #Merge args from request into kwargs
        #Kwargs is not overridden
        kwargs = self.mergeArgDict(kwargs,request_args,False)
        return kwargs
        
    def mergeArgDict(self,arg_dict,new_dict,override=False):
        for key in new_dict:
            if key in arg_dict and override == False:
                raise Exception("argument, %s, has already been processed" % key)
            arg_dict[key] = new_dict[key]
        return arg_dict


    def render(self,request,handle=False,**kwargs):
        """
        Callable function that returns the page's html
        """
        #Check auth
        if self.AUTH_REQUIRED and \
           not request.user.is_authenticated():
            return self.getAuthRedirect(request)

        #Get context
        context = self.fetch(request,**kwargs)
        
        #Check for redirect
        if type(context) == type(render_to_string(self.REDIRECT_TEMPLATE_PATH,{})):
            return context

        if type(context) != type({}):
            raise Exception("context must be a {} type")
        #Add self to context
        context["self"] = self
        context_instance = RequestContext(request,context)

        if self.TEMPLATE_PATH == None:
            raise Exception("must define a self.TEMPLATE_PATH")
        html = render_to_string(self.TEMPLATE_PATH,context,context_instance)

        if not handle:
            #Need to add container div
            context = {
                        "id": self.NAME+"_container",
                        "content": html,
                    }
            context_instance = RequestContext(request,context)
            html = render_to_string(self.CONTAINER_TEMPLATE_PATH,context,context_instance)
        
        return html


    def getAuthRedirect(self,request):
        next_json = ""
        context = {
                    "next_json": next_json,
                }
        context_instance = RequestContext(request,context)
        redirect = render_to_string(self.AUTH_REDIRECT_TEMPLATE_PATH,
                                    context,
                                    context_instance)
        return redirect


    def redirect(self,request,args):
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


    def fetch(self,request,**kwargs):
        """
        Gets data and creates context dict
        Override this function to make the context object
        """
        return {}
