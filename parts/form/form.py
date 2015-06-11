from djangoParts.parts.base_part import BasePart as Part
from djangoParts.parts.button import Button


class SubmitButton(Button):
    NAME = "submit_button"
    TITLE = "submit"
    SUBMIT = True    

class Form(Part):
    NAME = "form"
    TEMPLATE_PATH = "parts/form.html"
    TARGET_URL = None
    PART_LIST = [
                    SubmitButton(name=self.NAME),
                ]
    REMDER_PART_LIST = True

    def fetch(self,**kwargs):
        entry_list = []
        for part in self.PART_LIST:
            entry_html = part.render(kwargs)
            entry_list.append(entry_html)
        context = {
                    "entries": entry_list,
                }
        return context


class Entry(Part):
    TITLE = None
    PLACEHOLDER = None

    def fetch(self,**kwargs):
        value = self.getValue(**kwargs)
        context = {
                    "value": value,
                }
        return context

    def value(self,**kwargs):
        return kwargs.get(self.name)

    def getValue(self,**kwargs):
        return None



class Input(Entry):
    TEMPLATE_PATH = "parts/input.html"


class Money(Input):
    pass


class Select(Entry):
    TEMPLATE_PATH = "parts/select.html"
    OPTION_LIST = None
    VALUE_ATTRIBUTE = None
    TITLE_ATTRIBUTE = None

    def fetch(self,**kwargs):
        selected_value = self.getValue(self,**kwargs)
        option_list = []
        for result in self.OPTION_LIST:
            value = getattr(result,self.VALUE_ATTRIBUTE)
            title = getattr(result,self.TITLE_ATTRIBUTE)

            if selected_value != None and \
               selected_value == value:
                selected = True
            else:
                selected = False

            option = {
                        "value": value,
                        "title": title,
                        "selected": selected,
                    }
            option_list.append(option)

        context = {
                    "options": option_list,
                }
        return context


class Password(Entry):
    TEMPLATE_PATH = "parts/password.html"


class File(Entry):
    TEMPLATE_PATH = "parts/file.html"
    MULTIPLE = False


class Multiline(Entry):
    TEMPLATE_PATH = "parts/multiline.html"
    LINES = None
    def fetch2(self,request,**kwargs):
        if self.LINES == None:
            raise Exception("must define self.LINES")
        return {}
