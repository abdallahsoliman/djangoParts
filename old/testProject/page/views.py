from djangoParts.parts import Page as PagePart,\
                              Container
from index.views import Index


class PageContainer(Container):
    NAME = "page_container"
    PART_LIST = [
                    Index,
                ]

class Page(PagePart):
    ROOT_PART = PageContainer
