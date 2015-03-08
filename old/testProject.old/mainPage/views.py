from djangoParts.parts import Part, Page, Jquery
from djangoParts.parts.bootstrap import Js as BootstrapJs,\
                                        Css as BootstrapCss
from colors.views import Colors
from greenButton.views import GreenButton

class MainPageContents(Part):
    NAME = "main_page_contents"
    TEMPLATE_PATH = "mainPage/main_page.html"
    CHILD_LIST = [
                    Colors,
                    GreenButton,
                ]

    def fetch(self,request,*args,**kwargs):
        #Get the colors as default
        contents_html = Colors().render(request,*args,**kwargs)
        green_button_html = GreenButton().render(request,*args,**kwargs)
        return {
                "contents":contents_html,
                "green_button":green_button_html
            }

class MainPage(Page):
    REQUIREMENTS_LIST = [
                        Jquery,
                        BootstrapJs,
                        BootstrapCss,
                    ]
    CONTENTS_PART = MainPageContents
