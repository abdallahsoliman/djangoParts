from djangoParts.parts import Part


class GreenButton(Part):
    NAME = "green_button"
    TEMPLATE_PATH = "greenButton/green_button.html"
    TARGET = "colors"

    def fetch(self,request,*args,**kwargs):
        target = self.TARGET
        data = "'color=449d44'"
        return {
                "target": target,
                "data": data,
            }
