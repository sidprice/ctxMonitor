##########################################################################
#
#   COPYRIGHT Sid Price 2022
#
#   This file is part of ctxMonitor
#
#       ctxMonitor is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License Nersion 3 as published
#   by the Free Software Foundation .
#
#       ctxMonitor is distributed in the hope that it will be useful, but WITHOUT
#   ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#   FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License along with Foobar.
#               If not, see <https://www.gnu.org/licenses/>.
#
#   Utility functions for ctxMonitor.
#
#   Class for storing the variables and those variables enabled for monitoring
#
##########################################################################

from ctx_timing import CtxTiming
import json


class Variable:
    def __init__(self, name, address, period=CtxTiming.Period_Default, enable=False, content=None, monitored=False):
        super().__init__()

        self.name = name
        self.address = address
        self.period = period
        self.enable = enable
        self.content = content
        self.monitored = monitored

    @staticmethod
    def decode_variable(o):
        if Variable.__name__ in o:
            return Variable(name=o['name'], address=o['address'], period=o['period'], enable=o['enable'], monitored=o['monitored'])
        return o

    def copy(self):
        return Variable(name=self.name, address=self.address, period=self.period, enable=self.enable, content=self.content, monitored=self.monitored)
        
class VariableEncoder(json.JSONEncoder):
    def default(self, o):
        if (isinstance(o, Variable)):
            return {'name': o.name, 'address': o.address, 'period': o.period, 'enable': o.enable, 'monitored': o.monitored, o.__class__.__name__: True}
        else:
            return json.JSONEncoder(self, 0)
