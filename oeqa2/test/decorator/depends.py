from unittest import SkipTest
from functools import wraps

from . import OETestDecorator

def _skipTestDependency(case, depends):
    results = case.tc._results
    skipReasons = ['errors', 'failures', 'skipped']

    for reason in skipReasons:
        for test, _ in results[reason]:
            if test.id() in depends:
                raise SkipTest("Test case %s depends on %s and was in %s." \
                        % (case.id(), test.id(), reason))

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

    def setUp(self):
        _skipTestDependency(self.case, self.depends)
