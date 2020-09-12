##########################################################################
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

    def __init__(self):
        super().__init__()

    @staticmethod
    def period_from_text(text):
        return CtxTiming.Periods[text]
    
    @staticmethod
    def text_from_period(period):
        values = CtxTiming.Periods.values()
        values_list = list(values)
        print(values_list)
        try:
            index = values_list.index(period)
            result = list(CtxTiming.Periods)[index]
        except :
            result = 'Unknown'
        
        return result

