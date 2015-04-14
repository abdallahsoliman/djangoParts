from djangoParts.parts.basePart import BasePart

from django.conf.urls import patterns, include, url
from django.contrib import admin


class Page(BasePart):
    NAME = "page"
    TEMPLATE_PATH = "parts/page.html"
    ADMIN = True
    FAVICON_PATH = "parts/gear_icon.png"

    def fetch(self,request,**kwargs):
        content = self.PART_LIST[0]().render(request)
        context = {
                    "content": content,
                    "favicon_path": self.FAVICON_PATH,
                }
        return context
    
    def getUrls(self,PageDefinition):
        pattern_list = [""]

        #Append the admin url if option is set
        if self.ADMIN == True:
            pattern = url(r'^admin/', include(admin.site.urls))
            pattern_list.append(pattern)

        #Get definition of self
        pattern = url(r"^$",PageDefinition.as_view(),name=PageDefinition.NAME)
        pattern_list.append(pattern)

        pattern_list += self.makeUrl(PageDefinition)
        return patterns(*pattern_list)

    def makeUrl(self,part):
        pattern_list = []
        url_regex = r"^%s$" % part.NAME
        pattern = url(url_regex,part.as_view(),name=part.NAME)
        pattern_list.append(pattern)
        for child_part in part.PART_LIST:
            pattern_list += self.makeUrl(child_part)
        return pattern_list
