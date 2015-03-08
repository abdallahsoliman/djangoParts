from djangoParts.parts import Part,Container
from inner.views import Inner

class Index(Part):
    NAME = "index"
    TEMPLATE_PATH = "index/index.html"
    PART_LIST = [Inner]
