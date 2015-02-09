import logging
log = logging.getLogger(__name__)

from djangoParts.parts import Part

class Page(Part):
    TEMPLATE_PATH = "parts/page.html"
    CONTENTS_PART = None

    def __init__(self):
        Part.__init__(self)
        self.check()
        self.gatherRequirements()

    def check(self):
        if self.CONTENTS_PART == None:
            raise Exception("your page has not been given any self.CONTENTS_PART")

    def gatherRequirements(self):
        self.css_objects = []
        for css_class in self.REQUIRE_CSS:
            self.css_objects.append(css_class())
        self.js_objects = []
        for js_class in self.REQUIRE_JS:
            self.js_objects.append(js_class())

    
    def fetch(self,request,*args,**kwargs):
        css_html = ""
        for css_class in self.css_objects:
            css_html += css_class.render(request)
        js_html = ""
        for js_class in self.js_objects:
            js_html += js_class.render(request)

        contents_html = self.CONTENTS_PART().render(request,*args,**kwargs)
        return {
                "page_css":css_html,
                "page_js":js_html,
                "page_contents":contents_html,
            }
