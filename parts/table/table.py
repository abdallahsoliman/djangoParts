from djangoParts.parts.basePart import BasePart

class Table(BasePart):
    TEMPLATE_PATH = "parts/table.html"
    HEADER = None

    def fetch(self,request,rows=None,**kwargs):
        if rows == None:
            raise Exception("no data provided to template")

        context = {
                    "header": self.HEADER,
                    "rows": rows,
                }
        return context
