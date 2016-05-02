class OETestDecorator(object):
    case = None # Reference of OETestCase decorated

    def bind(self, case):
        self.case = case

from .depends import OETestDepends
from .oeid import OETestID
