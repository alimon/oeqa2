# Copyright (C) 2016 Intel Corporation
# Released under the MIT license (see COPYING.MIT)

import subprocess
import unittest
import sys
import time

from oeqa2.test.case import OETestCase

class PingTest(OETestCase):
    def test_ping(self):
        output = ''
        count = 0
        endtime = time.time() + 60
        while count < 5 and time.time() < endtime:
            proc = subprocess.Popen("ping -c 1 %s" % self.target.ip, shell=True, stdout=subprocess.PIPE)
            output += proc.communicate()[0]
            if proc.poll() == 0:
                count += 1
            else:
                count = 0
        self.assertEqual(count, 5, msg = "Expected 5 consecutive replies, got %d.\nping output is:\n%s" % (count,output))
