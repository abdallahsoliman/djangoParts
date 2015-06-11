from djangoParts.parts.basePart import BasePart


class Stylesheet(BasePart):
    NAME = "stylesheet"
    TEMPLATE_PATH = "parts/stylesheet.html"
    SOURCE = None

    def fetch(self,**kwargs):
        if self.SOURCE == None:
            raise Exception("must define self.SOURCE")

        if self.SOURCE[0:4] == "http":
            static = False
        else:
            static = True

        context = {
                    "source": self.SOURCE,
                    "static": static,
                }
        return context
