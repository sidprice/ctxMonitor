##########################################################################
#
#   Class for storing the variables enabled for monitoring
#
##########################################################################

class Variable(object):
    def __init__(self, name, address, period):
        super().__init__()

        self.name = name
        self.address = address
        self.period = period


