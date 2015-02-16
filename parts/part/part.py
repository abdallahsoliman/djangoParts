from django.template.loader import render_to_string
from django.template import RequestContext
from django.http import HttpResponse
from django.views.generic import View
from django.conf.urls import url as DjangoUrl


class Part(View):
    NAME = None
    TEMPLATE_PATH = None
    PART_TEMPLATE_PATH = "parts/part.html"
    CHILD_LIST = []
    REQUIREMENTS_LIST = []

    def __init__(self,parent_part=None):
        self.parent = parent_part
        self.check()
        self.makeName()
        self.makeUrl()

    def check(self):
        """
        Checks that all the things that should be added to every part are present.
        Throws exceptions if not all requirements have been given.
        """
        if self.NAME == None:
            raise Exception("tried to create a part without a self.NAME")
        if self.TEMPLATE_PATH == None:
            raise Exception("tried to create a part without a self.TEMPLATE_PATH")


    def get(self,request,*args,**kwargs):
        """
        takes arguments from url
        returns response with rendered html
        """
        html = self.render(request,*args,**kwargs)
        response = HttpResponse(html)
        return response

    def render(self,request,*args,**kwargs):
        """
        takes arguments
        fetches data
        reutrns rendered html
        """
        context = self.fetch(request,*args,**kwargs)
        #Check that context is a {} type
        if not type(context) == type({}):
            raise Exception("self.fetch did not return a {} type")
        context_inst = RequestContext(request,context)
        content = render_to_string(self.TEMPLATE_PATH,context,context_inst)

        loader_context = {
                            "name": self.name,
                            "target": self.name,
                            "target_url": self.url,
                        }
        context_inst = RequestContext(request,loader_context)
        loader_html = render_to_string("parts/loader.html",loader_context,context_inst)

        part_context = {
                        "name": self.name,
                        "content": content,
                        "loader": loader_html
                    }
        html = render_to_string(self.PART_TEMPLATE_PATH,part_context,context_inst)

        return html


    def fetch(self,request,*args,**kwargs):
        """
        takes arguments
        gets data from source
        returns context

        should usually be overridden
        """
        return {}


    def makeName(self):
        if self.parent == None:
            self.name = self.NAME
        else:
            self.name = self.parent.name+"__"+self.NAME

    def makeUrl(self):
        if self.parent == None:
            self.url = self.NAME
        else:
            self.url = self.parent.url+"/"+self.NAME
