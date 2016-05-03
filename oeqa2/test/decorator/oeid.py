from functools import wraps
from . import OETestDecorator

class OETestID(OETestDecorator):
    def __init__(self, oeid):
        oeidtype = type(oeid)
        if oeidtype is int:
            self.oeid = oeid
        else:
            raise TypeError("OETestID decorator expects int argument, received"\
                    " %s." % oeidtype)

    def __call__(self, func):
        @wraps(func)
        def wrapped_f(*args, **kwargs):
            self.oeid = self.oeid # For make visible in obj.cell_contents
            return func(*args, **kwargs)
        return wrapped_f

    def bind(self, case):
        super(OETestID, self).bind(case)
        case.oeid = self.oeid
