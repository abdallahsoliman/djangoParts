from django.template.loader import render_to_string
from django.template import RequestContext
from django.http import HttpResponse
from django.views.generic import View
from django.conf.urls import url as DjangoUrl


class Part(View):
    NAME = None
    TEMPLATE_PATH = None
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
        response = HttpResponse(self.render(request,*args,**kwargs))
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

        part_context = {
                        "name":self.name,
                        "content":content,
                    }
        return render_to_string("parts/part.html",part_context,context_inst)

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
