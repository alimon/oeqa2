class OETestDecorator(object):
    case = None # Reference of OETestCase decorated

    def bind(self, case):
        self.case = case
        self.case.decorators.append(self)

    def setUp(self):
        pass

from .depends import OETestDepends
from .oeid import OETestID
