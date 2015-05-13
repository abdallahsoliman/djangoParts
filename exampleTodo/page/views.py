from djangoParts.parts import Page as PagePart

from item.views import Item


class Page(PagePart):
    PART_LIST = [
                    Item,
                ]
