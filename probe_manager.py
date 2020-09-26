##########################################################################
#
#   This class manages the connection with the probe and does the 
#   variable monitoring as requested.
#
##########################################################################

from ctx_pubsub import Ctx_PubSub

class ProbeManager():
    __instance = None

    @staticmethod
    def getInstance():
        '''
            Static Access method
        '''
        if ProbeManager.__instance == None:
            ProbeManager()
        return ProbeManager.__instance

    def __init__(self):
        '''
            Virtually private constructor
        '''
        if ProbeManager.__instance != None:
            raise Exception('This class is a singleton, use getInstance')
        else:
            ProbeManager.__instance = self
      
        ###
        #
        #   Subscribe to variable monitor requests
        #
        ###
        self._pubSub = Ctx_PubSub.getInstance()
        self._pubSub.subscribe_monitor_variable(self._listener_monitor_variable)

    def _listener_monitor_variable(self, monitor):
        pass
