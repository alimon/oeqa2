import unittest

class OETestCase(unittest.TestCase):
    decorators = []

    def __init__(self, tc, methodName='runTest', *args, **kwargs):
        super(OETestCase, self).__init__(methodName)
        self.tc = tc

    def setUp(self):
        for d in self.decorators:
            d.setUp()
