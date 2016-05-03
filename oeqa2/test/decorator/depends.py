from functools import wraps
from . import OETestDecorator

class OETestDepends(OETestDecorator):
    def __init__(self, depends):
        dtype = type(depends)
        if dtype is str:
            self.depends = [depends]
        elif dtype is tuple or dtype is list:
            self.depends = depends
        else:
            raise TypeError("OETestDepends decorator expects str, tuple or list"\
                    " argument, received %s." % dtype)

    def __call__(self, func):
        @wraps(func)
        def wrapped_f(*args, **kwargs):
            self.depends = self.depends # For make visible in obj.cell_contents
            return func(*args, **kwargs)
        return wrapped_f
