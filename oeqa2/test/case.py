import unittest

class OETestCase(unittest.TestCase):
    def __init__(self, tc, methodName='runTest', *args, **kwargs):
        super(OETestCase, self).__init__(methodName)
        self.tc = tc
