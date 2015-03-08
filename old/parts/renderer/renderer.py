from django.template import RequestContext
from django.template.loader import render_to_string


class Renderer:
    NAME = None
    TEMPLATE_PATH = None


    def __init__(self):
        self.check()


    def check(self):
        """
        Throws exceptions if not all requirements have been given.
        """
        if self.NAME == None:
            raise Exception("tried to create a renderer without a self.NAME")
        if self.TEMPLATE_PATH == None:
            raise Exception("tried to create a renderer without a self.TEMPLATE_PATH")
            

    def render(self,request,**kwargs):
        context = self.fetch(request,**kwargs)
        if not type(context) == type({}):
            raise Exception("self.fetch did not return a {} type")
        context_instance = RequestContext(request,context)
        rendered_html = render_to_string(self.TEMPLATE_PATH,context,context_instance)
        return rendered_html


    def fetch(request,**kwargs):
        """
        takes arguments
        gets data from source
        returns context

        should usually be overridden
        """
        return {}
