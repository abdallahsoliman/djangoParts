from djangoParts.parts import Part


class Container(Part):
    TEMPLATE_PATH = "parts/container.html"
    PARENT_NAME = None
    PART_LIST = None

    def __init__(self):
        self.name = "_".join([self.PARENT_NAME,self.NAME])
        Part.__init__(self)

    def fetch(self,request,**kwargs):
        return {"self":self}
