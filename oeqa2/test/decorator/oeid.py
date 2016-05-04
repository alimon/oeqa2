from . import OETestDecorator

class OETestID(OETestDecorator):
    attrs = {
            'oeid' : int
    }

    def bind(self, case):
        super(OETestID, self).bind(case)
        case.oeid = self.oeid
