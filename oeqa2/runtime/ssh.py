import subprocess
import unittest
import sys

from oeqa2.test.case import OETestCase
from oeqa2.test.decorator import OETestDepends, OETestID

class SshTest(OETestCase):
    @OETestDepends('test_ssh_10')
    def test_ssh_20(self):
        pass

    @OETestDepends(('test_ssh'))
    def test_ssh_10(self):
        pass

    @OETestID(224)
    @OETestDepends('ping.PingTest.test_ping')
    def test_ssh(self):
        (status, output) = self.target.run('uname -a')
        self.assertEqual(status, 0, msg="SSH Test failed: %s" % output)
        (status, output) = self.target.run('cat /etc/masterimage')
        self.assertEqual(status, 1, msg="This isn't the right image  - /etc/masterimage shouldn't be here %s" % output)

