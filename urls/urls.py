import logging
log = logging.getLogger(__name__)

from django.conf.urls import url as DjangoUrl


class Urls:
    def __init__(self,url_list):
        self.url_list = url_list

    def make(self,Part,parent_part=None):
        if parent_part:
            part = Part(parent_part)
        else:
            part = Part()
        regex = r"^%s$" % part.url
        part_url = DjangoUrl(regex,Part.as_view(),name=part.name)
        self.url_list.append(part_url)
        for child in part.CHILD_LIST:
            self.make(child_obj,part)
        return self.url_list
