from djangoParts.parts import Part


class Container(Part):
    TEMPLATE_PATH = "parts/container.html"

    def __init__(self):
        self.name = self.NAME+"_container"
        Part.__init__(self)

    def fetch(self,request,**kwargs):
        return {"self":self}
