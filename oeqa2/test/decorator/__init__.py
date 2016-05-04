from functools import wraps

class OETestDecorator(object):
    case = None # Reference of OETestCase decorated
    attrs = None # Attributes to be loaded by decorator implementation

    def __init__(self, *args, **kwargs):
        if not self.attrs:
            return

        for idx, attr in enumerate(self.attrs):
            attr_type = self.attrs[attr]

            if attr in kwargs:
                value = kwargs[attr]
            else:
                value = args[idx]

            value_type = type(value)
            if not value_type == attr_type:
                class_name = self.__class__.__name__
                raise TypeError("%s decorator attr %s expects argument %s"\
                        " received %s." % (class_name, attr, attr_type,
                        value_type))

            setattr(self, attr, value)

    def __call__(self, func):
        @wraps(func)
        def wrapped_f(*args, **kwargs):
            self.attrs = self.attrs # XXX: Enables OETestLoader discover
            return func(*args, **kwargs)
        return wrapped_f

    def bind(self, case):
        self.case = case
        self.case.decorators.append(self)

    def setUp(self):
        pass

from .depends import OETestDepends
from .oeid import OETestID
