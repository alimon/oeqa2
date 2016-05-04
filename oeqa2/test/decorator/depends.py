from unittest import SkipTest

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
    attrs = {
            'depends': list
    }

    def setUp(self):
        _skipTestDependency(self.case, self.depends)
