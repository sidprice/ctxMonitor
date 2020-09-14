##########################################################################
#
#   Class for storing the variables and those variables enabled for monitoring
#
##########################################################################

from ctx_timing import CtxTiming
import json


class Variable:
    def __init__(self, name, address, period=CtxTiming.Period_Default, enable=True):
        super().__init__()

        self.name = name
        self.address = address
        self.period = period
        self.enable = enable

    @staticmethod
    def decode_variable(o):
        if Variable.__name__ in o:
            return Variable(name=o['name'], address=o['address'], period=o['period'], enable=o['enable'])
        return o


class VariableEncoder(json.JSONEncoder):
    def default(self, o):
        if (isinstance(o, Variable)):
            return {'name': o.name, 'address': o.address, 'period': o.period, 'enable': o.enable, o.__class__.__name__: True}
        else:
            return json.JSONEncoder(self, 0)
