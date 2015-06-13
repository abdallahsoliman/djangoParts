from djangoParts.parts.basePart import BasePart as Part
from djangoParts.parts.button import Button


class SubmitButton(Button):
    NAME = "submit_button"
    TITLE = "submit"
    SUBMIT = True
    CLASS = "btn btn-success"

class Form(Part):
    NAME = "form"
    TEMPLATE_PATH = "parts/form/form.html"
    TARGET_URL = None
    ENTRY_LIST = None
    SUBMIT_BUTTON = SubmitButton(prefix=NAME)

    def fetch(self,**kwargs):
        if self.ENTRY_LIST == None:
            raise Exception("must define self.ENTRY_LIST")
        if self.TARGET_URL == None:
            raise Exception("must define self.TARGET_URL")

        entry_list = []
        for part in self.ENTRY_LIST:
            entry_html = part(self.name).render(**kwargs)
            entry_list.append(entry_html)
        context = {
                    "entries": entry_list,
                    "submit_button": self.SUBMIT_BUTTON.render(**kwargs)
                }
        return context

    def readValues(self,**kwargs):
        value_dict = {}
        for entry in self.ENTRY_LIST:
            entry = entry(self.name)
            value = entry.readValue(**kwargs)
            if value == None:
                continue
            value_dict[entry.NAME] = value
        return value_dict


class Entry(Part):
    TITLE = None
    PLACEHOLDER = None

    def fetch(self,**kwargs):
        value = self.getValue(**kwargs)
        context = {
                    "value": value,
                }
        return context

    def readValue(self,**kwargs):
        """
        Reads value from request
        """
        return kwargs.get(self.NAME)

    def getValue(self,value=None,**kwargs):
        """
        Reads value from arguments
        """
        return value



class Input(Entry):
    TEMPLATE_PATH = "parts/form/input.html"


class Money(Input):
    pass


class Select(Entry):
    TEMPLATE_PATH = "parts/form/select.html"
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
    TEMPLATE_PATH = "parts/form/password.html"


class File(Entry):
    TEMPLATE_PATH = "parts/form/file.html"
    MULTIPLE = False


class Multiline(Entry):
    TEMPLATE_PATH = "parts/form/multiline.html"
    LINES = None
    def fetch2(self,request,**kwargs):
        if self.LINES == None:
            raise Exception("must define self.LINES")
        return {}
