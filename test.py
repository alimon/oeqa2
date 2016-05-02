#!/usr/bin/env python

import unittest
import logging

logging.basicConfig(
    level=logging.DEBUG
)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG - 2)
logger.addHandler(logging.NullHandler())
d = None

from oeqa2.test.context import OETestContext

tctx = OETestContext(d, logger)
tctx.loadTests('oeqa2/runtime/')
tctx.runTests()
