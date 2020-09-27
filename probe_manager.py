##########################################################################
#
#   This class manages the connection with the probe and does the 
#   variable monitoring as requested.
#
##########################################################################

from ctx_pubsub import Ctx_PubSub
from PyQt5.QtCore import QTime, QTimer
from ctx_timing import CtxTiming

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

    ###
    #
    #   Define the tick period for the timer
    #
    ###
    #_tick_period = CtxTiming.Timer_Period
    _tick_period = 2000

    _monitored_variables = {}
    _monitor_timers = {}
    
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
        #   Create the timer that will drive the variable reading
        #
        ###
        self._timer = QTimer()
        self._timer.timeout.connect(self._timer_tick)
        self._timer.start(self._tick_period)
        ###
        #
        #   Subscribe to variable monitor requests
        #
        ###
        self._pubSub = Ctx_PubSub.getInstance()
        self._pubSub.subscribe_monitor_variable(self._listener_monitor_variable)
        self._pubSub.subscribe_monitored_database(self._listener_monitor_database)

    def _listener_monitor_database(self, monitored):
        self._monitored_variables = dict(monitored)
        self._updateMonitorTimers()

    def _listener_monitor_variable(self, monitor):
        ###
        #
        #   check if the variable is in the local database and
        #   update it if found.
        #
        #   otherwise add it
        #
        ###
        found =False
        for name, var in self._monitored_variables.items():
            if monitor.name == name:
                ###
                #
                #   Update the monitored variable
                #
                ###
                var.address = monitor.address
                var.period = monitor.period
                var.enable = monitor.enable
                found = True
                break
        if (found == False):
            self._monitored_variables[monitor.name] = monitor
        self._updateMonitorTimers()

    def _updateMonitorTimers(self):
        self._monitor_timers = {}
        for name, var in self._monitored_variables.items():
            self._monitor_timers[name] = var.period
        print(self._monitor_timers)

    def _timer_tick(self):
        for name, var in self._monitored_variables.items():
            print(f'{var.name} {var.address} {var.enable}')
        print('--+++++--')


