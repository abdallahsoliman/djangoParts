import logging
log = logging.getLogger(__name__)

from djangoParts.parts import Part

class Css(Part):
    TEMPLATE_PATH = "parts/css.html"
    HREF = None

    def fetch(self,*args,**kwargs):
        if self.HREF == None:
            raise Exception("css object was not given self.HREF")
        return {"href":self.HREF}
