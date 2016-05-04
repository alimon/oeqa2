import unittest
import logging

class OEStreamLogger(object):
    def __init__(self, logger):
        self.logger = logger

    def write(self, msg):
        for line in msg.rstrip().splitlines():
            self.logger.log(logging.INFO, line.rstrip())

    def flush(self):
        for handler in self.logger.handlers:
            handler.flush()

class OETestResult(unittest.TextTestResult):
    def __init__(self, tc, *args, **kwargs):
        super(OETestResult, self).__init__(*args, **kwargs)

        self.tc = tc

        self.tc._results['failures'] = self.failures
        self.tc._results['errors'] = self.errors
        self.tc._results['skipped'] = self.skipped
        self.tc._results['expectedFailures'] = self.expectedFailures

    def startTest(self, test):
        super(OETestResult, self).startTest(test)

class OETestRunner(unittest.TextTestRunner):
    resultclass = OETestResult

    def __init__(self, tc, *args, **kwargs):
        super(OETestRunner, self).__init__(*args, **kwargs)
        self.tc = tc

    def _makeResult(self):
        return self.resultclass(self.tc, self.stream, self.descriptions,
                self.verbosity)
