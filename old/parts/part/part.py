from django.views.generic import GenericView
from django.template import RequestContext
from django.template.loader import render_to_string
from django.http import HttpResponse


class Part(GenericView):
    NAME = None
    TEMPLATE_PATH = None

    CONTAINER_TEMPLATE_PATH = "part/container.html"
    JS_TAG_TEMPLATE_PATH = "part/js_tag.html"

    def __init__(self,container_name=None):
        GenericView.__init__(self)
        self.check()
        self.container_name = container_name

    def check(self):
        """
        Throws exceptions if not all requirements have been given.
        """
        #Make sure there is a name
        if self.NAME == None:
            raise Exception("tried to create a renderer without a self.NAME")
        #Make sure that there is a template
        if self.TEMPLATE_PATH == None:
            raise Exception("tried to create a renderer without a self.TEMPLATE_PATH")


    def get(self,request,*args,**kwargs):
        #TODO: permissions
        html = self.render(request,**kwargs)
        response = HttpResponse(html)
        return response

    def post(self,request,*args,**kwargs):
        #TODO: permissions
        self.save(request,**kwargs)
        response = HttpResponse("<h1>swrv</h1>")
        return response


    def render(self,request,**kwargs):
        context = self.fetch(request,**kwargs)
        if not type(context) == type({}):
            raise Exception("self.fetch did not return a {} type")
        context_instance = RequestContext(request,context)
        rendered_html = render_to_string(self.TEMPLATE_PATH,context,context_instance)
        
        container_context = {
                                "container_name":self.container_name,
                                "contents": rendered_html,
                            }
        container_context_instance = RequestContext(request,container_context)
        container_html = render_to_string(self.CONTAINER_TEMPLATE_PATH,container_context,container_context_instance)
        #js_tag = render_to_string
        return container_html

    def fetch(request,**kwargs):
        """
        takes arguments
        gets data from source
        returns context

        should usually be overridden
        """
        return {}

    def save(request,**kwargs):
        return
