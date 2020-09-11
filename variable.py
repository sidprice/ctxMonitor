##########################################################################
#
#   Class for storing the variables and those variables enabled for monitoring
#
##########################################################################

class Variable(object):
    def __init__(self, name, address, period=0,):
        super().__init__()

        self.name = name
        self.address = address
        self.period = period


