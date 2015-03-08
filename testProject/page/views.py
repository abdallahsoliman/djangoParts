from djangoParts.parts import Page as PagePart,\
                              Container
from index.views import Index
from info.views import Info


class PageContainer(Container):
    NAME = "page_container"
    PARENT_NAME = "page"
    PART_LIST = [
                    Index,
                    Info,
                ]

class Page(PagePart):
    PAGE_CONTAINER = PageContainer
    CONTAINER_LIST = [PageContainer]
