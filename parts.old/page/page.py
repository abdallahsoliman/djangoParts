import logging
log = logging.getLogger(__name__)

from djangoParts.parts import Part

class Page(Part):
    TEMPLATE_PATH = "parts/page.html"
    PART_TEMPLATE_PATH = "parts/requirement.html"
    CONTENTS_PART = None
    NAME = ""
    CHILD_LIST = []

    def __init__(self):
        Part.__init__(self)
        self.check()
        self.CHILD_LIST.append(self.CONTENTS_PART)

    def check(self):
        Part.check(self)
        if self.CONTENTS_PART == None:
            raise Exception("your page has not been given any self.CONTENTS_PART")

    def fetch(self,request,*args,**kwargs):
        requirements_list = self.REQUIREMENTS_LIST
        #Get the requirements from all children
        requirements_list += self.gatherRequirements(self.CONTENTS_PART)

        css_html = ""
        for css_class in requirements_list:
            css_html += css_class().render(request)
        js_html = ""
        #for js_class in self.js_objects:
        #    js_html += js_class.render(request)

        contents_html = self.CONTENTS_PART().render(request,*args,**kwargs)
        return {
                "page_css":css_html,
                "page_js":js_html,
                "page_contents":contents_html,
            }

    def gatherRequirements(self,Part):
        requirements_list = Part.REQUIREMENTS_LIST
        for ChildPart in Part.CHILD_LIST:
            requirements_list += self.gatherRequirements(ChildPart)
        return requirements_list
