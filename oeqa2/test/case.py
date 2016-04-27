import unittest

class OETestCase(unittest.TestCase):
    def __init__(self, tc, methodName='runTest', *args, **kwargs):
        super(OETestCase, self).__init__(methodName)
        self.tc = tc

    def oe_id(self):
        return "%s.%s" % (self.__module__, self.id())
