import logging
log = logging.getLogger(__name__)

from djangoParts.parts import Js as JsPart


class Js(JsPart):
    NAME = "bootstrap_js"
    SRC = "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.2/js/bootstrap.min.js"
