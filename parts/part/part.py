from django.template.loader import render_to_string
from django.template import RequestContext
from django.http import HttpResponse
from django.views.generic import View

class Part(View):
    def get(self,request,*args,**kwargs):
        return HttpResponse(self.render(request,*args,**kwargs))

    def render(self,request,*args,**kwargs):
        context = self.fetch(request,*args,**kwargs)
        #TODO: check that context is a {} type
        context_inst = RequestContext(request,context)
        return render_to_string(self.TEMPLATE_PATH,context,context_inst)

    def fetch(self,request,*args,**kwargs):
        return {}
