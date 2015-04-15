from djangoParts.parts import Part,Container
from inner.views import Inner
from info.views import Info

class IndexOptions(Container):
    NAME = "index_options"
    PART_LIST = [Info,Inner]

class Index(Part):
    NAME = "index"
    TEMPLATE_PATH = "index/index.html"
    PART_LIST = [IndexOptions]
