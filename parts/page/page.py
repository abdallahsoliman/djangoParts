import logging
log = logging.getLogger(__name__)

from fapengine.fedj.parts import Part

class Page(Part):
    TEMPLATE_PATH = "parts/page.html"
    
    def fetch(self,request,*args,**kwargs):
        css = self.REQUIRE_CSS
        js = self.REQUIRE_JS

        css_html = ""
        for css_class in css:
            css_html += css_class().render(request)
        js_html = ""
        for js_class in js:
            js_html += js_class().render(request)

        contents_html = self.getContents(request,*args,**kwargs)
        return {
                "page_css":css_html,
                "page_js":js_html,
                "page_contents":contents_html,
            }
