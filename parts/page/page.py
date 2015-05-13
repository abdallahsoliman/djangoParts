from djangoParts.parts.basePart import BasePart

from django.conf.urls import patterns, include, url
from django.contrib import admin


class Page(BasePart):
    NAME = "page"
    TEMPLATE_PATH = "parts/page.html"
    DJANGO_ADMIN = True
    FAVICON_PATH = "parts/gear_icon.png"

    def fetch(self,request,**kwargs):
        content = self.getContent(request,kwargs)
        context = {
                    "content": content,
                    "favicon_path": self.FAVICON_PATH,
                }
        return context

    def getContent(self,request,kwargs):
        content_part = self.getContentPart(kwargs)
        if content_part == False:
            content = ""
        else:
            content = content_part().render(request,**kwargs)
        return content

    def getContentPart(self,kwargs):
        if len(self.PART_LIST) == 0:
            return False

        if "test_part" in kwargs:
            part_name = kwargs["test_part"]
            test_part = self.getTestPart(self,part_name)
            if not test_part:
                raise Exception("could not find test part %s" % part_name)
            return test_part

        if "page" in kwargs:
            part_dict = self.getPartDict()
            return part_dict[kwargs["page"]]
        else:
            return self.PART_LIST[0]

        raise Exception("could not find a part to render into page")


    def getTestPart(self,part,part_name):
        if part.NAME == part_name:
            return part
        for child_part in part.PART_LIST:
            test_part = self.getTestPart(child_part,part_name)
            if test_part:
                return test_part
        

    def getPartDict(self):
        part_dict = {}
        for part in self.PART_LIST:
            part_dict[part.NAME] = part
        return part_dict
    
    def getUrls(self,PageDefinition):
        pattern_list = [""]

        #Append the admin url if option is set
        if self.DJANGO_ADMIN == True:
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
