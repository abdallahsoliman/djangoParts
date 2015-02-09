from django.template.loader import render_to_string
from django.template import RequestContext
from django.http import HttpResponse
from django.views.generic import View

class Part(View):
    NAME = None
    TEMPLATE_PATH = None

    def __init__(self):
        self.check()

    def check(self):
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
        response.__setitem__("Access-Control-Allow-Origin", "*")
        return response

    def render(self,request,*args,**kwargs):
        """
        takes arguments
        fetches data
        reutrns rendered html
        """
        context = self.fetch(request,*args,**kwargs)
        #TODO: check that context is a {} type
        context_inst = RequestContext(request,context)
        content = render_to_string(self.TEMPLATE_PATH,context,context_inst)

        part_context = {
                        "name":self.NAME,
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
