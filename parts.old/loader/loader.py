import logging
log = logging.getLogger(__name__)

from djangoParts.parts import Part


class Loader(Part):
    NAME = "loader"
    TEMPLATE_PATH = "parts/loader.html"

    def __init__(self,target,target_url):
        self.target = target
        self.target_url = target_url

    def fetch(self,request,*args,**kwargs):
        return {
                "target": target,
                "target_url": target_url,
            }
