import logging
log = logging.getLogger(__name__)

from djangoParts.parts import Css as CssPart


class Css(CssPart):
    NAME = "bootstrap_css"
    HREF = "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css"
