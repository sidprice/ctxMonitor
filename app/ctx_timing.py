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
#   Class that provides the timing features for ctxMonitor
#
##########################################################################

class CtxTiming(object):
    ###
    #
    #   Define the ComboBox entries
    #
    ###

    Periods = {
        '100mS': 100,
        '200mS': 200,
        '500mS': 500,
        '1 Second': 1000,
        '2 Seconds': 2000,
        '5 Seconds': 5000,
        '10 Seconds': 10000
    }

    Period_Default = 100
    Timer_Period = 100
    
    def __init__(self):
        super().__init__()

    @staticmethod
    def period_from_text(text):
        return CtxTiming.Periods[text]
    
    @staticmethod
    def text_from_period(period):
        values = CtxTiming.Periods.values()
        values_list = list(values)

        try:
            index = values_list.index(period)
            result = list(CtxTiming.Periods)[index]
        except :
            result = 'Unknown'
        
        return result

