from djangoParts.parts import Part
from info.views import Info

class Inner(Part):
    NAME = "inner"
    TEMPLATE_PATH = "inner/inner.html"
    PART_LIST = [Info]
