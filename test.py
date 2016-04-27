#!/usr/bin/env python

import unittest
import logging

logger = logging.getLogger()
d = None

from oeqa2.test.context import OETestContext

tctx = OETestContext(d, logger)
tctx.loadTests('oeqa2/runtime/')
tctx.runTests()
