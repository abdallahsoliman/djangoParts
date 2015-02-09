import logging
log = logging.getLogger(__name__)

from djangoParts.parts import Part

class Js(Part):
    TEMPLATE_PATH = "parts/js.html"
    SRC = None

    def fetch(self,*args,**kwargs):
        if self.SRC == None:
            raise Exception("js object was not given self.SRC")
        return {"src":self.SRC}
