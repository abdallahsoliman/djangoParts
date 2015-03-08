from django.views.generic import View as GenericView
from django.http import HttpResponse
from django.template import RequestContext
from django.template.loader import render_to_string


class Part(GenericView):
    NAME = None
    TEMPLATE_PATH = None
    CONTAINER_LIST = None


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


    #HTTP functions that are exposed

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


    #Parts functions that support the HTTP functions
    
    def render(self,request,**kwargs):
        context = self.fetch(request,**kwargs)
        if not type(context) == type({}):
            raise Exception("self.fetch did not return a {} type")
        context_instance = RequestContext(request,context)
        #Render main html
        rendered_html = render_to_string(self.TEMPLATE_PATH,context,context_instance)
        #Render scripts to load any containers
        rendered_html += render_to_string("parts/part_list_load_functions.html",
                                          {"self":self},
                                          context_instance)
        return rendered_html

    def fetch(self,request,**kwargs):
        """
        takes arguments
        gets data from source
        returns context

        should usually be overridden
        """
        return {}


    def save(request,**kwargs):
        return
