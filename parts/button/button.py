from djangoParts.parts.basePart import BasePart as Part


class Button(Part):
    NAME = "button"
    TEMPLATE_PATH = "parts/button.html"
    CLASS = "btn btn-default"
    TARGET_URL = None
    SUBMIT = False
    TITLE = None

    def fetch(self,**kwargs):
        if self.TARGET_URL and self.SUBMIT:
            raise Exception("cannot have a button that submits its own form and also has a target url")
        if not self.TITLE:
            raise Exception("must provide self.TITLE")
        return {}
