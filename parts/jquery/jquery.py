import logging
log = logging.getLogger(__name__)

from djangoParts.parts import Js


class Jquery(Js):
    NAME = "jquery_js"
    SRC = "https://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"
