##########################################################################
#
#   Class for storing the variables and those variables enabled for monitoring
#
##########################################################################

from ctx_timing import CtxTiming

class Variable(object):
    def __init__(self, name, address, period=CtxTiming.Period_Default):
        super().__init__()

        self.name = name
        self.address = address
        self.period = period


