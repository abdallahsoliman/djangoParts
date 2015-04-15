from djangoParts.parts import Part, Page as PagePart


class Main(Part):
    NAME = "main"
    TEMPLATE_PATH = "page/page.html"

    def fetch(self,request,**kwargs):
        page = "default"

        get_data = request.GET
        if "page" in get_data:
            page = get_data["page"]

        return {"page": page}


class Page(PagePart):
    ROOT_PART = Main
