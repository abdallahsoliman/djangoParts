from djangoParts.parts import Part

from django.conf.urls import patterns, include, url
from django.contrib import admin


class Page(Part):
    NAME = "page"
    TEMPLATE_PATH = "parts/page.html"
    ROOT_PART = None

    def __init__(self):
        self.check()
        self.PART_LIST = [self.ROOT_PART]


    def check(self):
        Part.check(self)
        if self.ROOT_PART == None:
            raise Exception("must define self.ROOT_PART")
        if self.PART_LIST != None:
            raise Exception("Page part cannot have self.PART_LIST defined because it makes its own")

    def getUrls(self,part,root=True):
        #TODO: Admin support
        url_list = []

        #Add this url to the url_list
        if root == True:
            part_name = ""
        else:
            part_name = part.NAME
        url_pattern = "^%s$" % part_name
        new_url = url(url_pattern,part.as_view(),name=part.NAME)
        url_list.append(new_url)

        #Add the children to the url_list
        part_instance = part()
        if part_instance.PART_LIST != None:
            for child_part in part_instance.PART_LIST:
                url_list += self.getUrls(child_part,root=False)

        #Recurse to find addtional urls
        if root == False:
            return url_list
        #If this is the root iteration, then make the patterns
        else:
            return patterns("",*url_list)
