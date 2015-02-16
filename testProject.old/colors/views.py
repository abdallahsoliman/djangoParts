from djangoParts.parts import Part


class Colors(Part):
    NAME = "colors"
    TEMPLATE_PATH = "colors/colors.html"

    def fetch(self,request,color="FFF000"):
        if "color" in request.GET:
            color = request.GET["color"]
        return {"color": color}
