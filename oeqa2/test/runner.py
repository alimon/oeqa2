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
    def startTest(self, test):
        super(OETestResult, self).startTest(test)

class OETestRunner(unittest.TextTestRunner):
    resultclass = OETestResult
