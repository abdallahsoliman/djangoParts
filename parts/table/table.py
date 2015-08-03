from djangoParts.parts.basePart import BasePart

class Table(BasePart):
    NAME = "table"
    TEMPLATE_PATH = "parts/table.html"
    HEADER = None
    CLASS = "table"

    def fetch(self,body=None,**kwargs):
        if body == None:
            raise Exception("no data provided to table")

        context = {
                    "header": self.HEADER,
                    "body": body,
                }
        return context
