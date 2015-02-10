from djangoParts.parts import Part, Page, Jquery
from djangoParts.parts.bootstrap import Js as BootstrapJs,\
                                        Css as BootstrapCss

class MainPageContents(Part):
    NAME = "main_page_contents"
    TEMPLATE_PATH = "mainPage/main_page.html"

class MainPage(Page):
    REQUIREMENTS_LIST = [
                        Jquery,
                        BootstrapJs,
                        BootstrapCss,
                    ]
    CONTENTS_PART = MainPageContents
