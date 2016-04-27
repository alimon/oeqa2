import os
import sys

from oeqa2.test.loader import OETestLoader
from oeqa2.test.runner import OETestRunner

class OETestContext(object):
    loaderClass = OETestLoader
    runnerClass = OETestRunner

    def __init__(self, d, logger):
        self.d = d
        self.logger = logger

    def _read_modules_from_manifest(self, manifest):
        if not os.path.exists(manifest):
            raise

        modules = []
        for line in open(manifest).readlines():
            line = line.strip()
            if line and not line.startswith("#"):
                modules.append(line)

        return modules

    def loadTests(self, module_path, modules=[], 
            modules_manifest="", modules_required=[]):
        if modules_manifest:
            modules = self._read_modules_from_manifest(modules_manifest)

        self.loader = self.loaderClass(self, module_path, modules, modules_required)
        self.suites = self.loader.discover()

    def runTests(self):
        self.runner = self.runnerClass()
        self.runner.run(self.suites)
