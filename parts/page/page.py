from djangoParts.parts import Part

from django.conf.urls import patterns, include, url
from django.contrib import admin


class Page(Part):
    NAME = "page"
    TEMPLATE_PATH = "parts/page.html"
    PAGE_CONTAINER = None


    def check(self):
        Part.check(self)
        if self.PAGE_CONTAINER == None:
            raise Exception("must define the page contianer")

    def getUrls(self,root_part=None):
        return
