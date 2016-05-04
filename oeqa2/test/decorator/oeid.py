# Copyright (C) 2016 Intel Corporation
# Released under the MIT license (see COPYING.MIT)

from . import OETestDecorator

class OETestID(OETestDecorator):
    attrs = {
            'oeid' : int
    }

    def bind(self, case):
        super(OETestID, self).bind(case)
        case.oeid = self.oeid
