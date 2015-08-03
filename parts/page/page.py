from djangoParts.parts.basePart import BasePart

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


class Page(BasePart):
    NAME = "page"
    TEMPLATE_PATH = "parts/page.html"
    DJANGO_ADMIN = True
    FAVICON_PATH = "parts/gear_icon.png"
    TRACKING_PATH = None
    HEAD_LIST = []

    def fetch(self,**kwargs):
        content = self.getContent(kwargs)

        if self.TRACKING_PATH:
            tracking_html = self.renderToString(self.TRACKING_PATH,{})
        else:
            tracking_html = False

        head_list = self.getHeadList(kwargs)
        print head_list

        context = {
                    "content": content,
                    "favicon_path": self.FAVICON_PATH,
                    "tracking": tracking_html,
                    "head_list": head_list,
                }
        return context

    def getContent(self,kwargs):
        content_part = self.getContentPart(kwargs)
        if content_part == False:
            content = ""
        else:
            content = content_part(prefix=self.name).render(**kwargs)
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
            part_dict = self.makePartDict()
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


    def makePartDict(self):
        part_dict = {}
        for part in self.PART_LIST:
            part_dict[part.NAME] = part
        return part_dict
        

    def getUrls(self):
        pattern_list = [""]

        #Append the admin url if option is set
        if self.DJANGO_ADMIN == True:
            pattern = url(r'^admin/', include(admin.site.urls))
            pattern_list.append(pattern)

        #Get definition of self
        pattern = url(r"^$",type(self).as_view(),name=self.NAME)
        pattern_list.append(pattern)

        pattern_list += self.makePatterns(type(self))
        url_patterns = patterns(*pattern_list)
        
        #Add development media url
        if settings.MEDIA_URL and settings.MEDIA_ROOT:
            url_patterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

        return url_patterns

    def makePatterns(self,part):
        url_regex = r"^%s$" % part.NAME
        pattern = url(url_regex,part.as_view(),name=part.NAME)
        pattern_list = [pattern]
        for child_part in part.PART_LIST:
            pattern_list += self.makePatterns(child_part)
        return pattern_list

    def getHeadList(self,kwargs):
        head_list = []
        for head_part in self.HEAD_LIST:
            head_list.append(head_part().render(**kwargs))
        return head_list
