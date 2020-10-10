##########################################################################
#
#   This class manages the connection with the probe and does the 
#   variable monitoring as requested.
#
##########################################################################

from ctx_pubsub import Ctx_PubSub
from PyQt5.QtCore import QTime, QTimer
from ctx_timing import CtxTiming
from variable import Variable
from probe import Probe

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
    _tick_period = CtxTiming.Timer_Period
    #_tick_period = 2000

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
        # TODO Need to subscribe to what vars to monitor
        # self._pubSub.subscribe_add_monitor_variable(self._listener_monitor_variable)
        # self._pubSub.subscribe_monitored_database(self._listener_monitor_database)

    def connect_to_probe(self):
        self._probe = Probe('COM8')
        if (self._probe.Connect()):
            print('Connected')
            ###
            #
            #   Scan the target
            #
            ###
            self._probe.sendCommand('s')
            while True:
                '''
                    Loop here reading resonses until "OK" is received
                '''
                response = self._probe.getResponse()
                if response != None:
                    if response == "OK":
                        break
                    print(response, end=' ')
            self._probe.sendCommand('vAttach;1', False)
            response = self._probe.getResponse()
            print(response)
        else:
            print('Connect failed')

    def _listener_monitor_database(self, monitored):
        self._monitored_variables = {}
        for name, var in monitored.items():
            newVar = Variable(var.name, var.address, var.period, var.enable)
            self._monitored_variables[name] = newVar
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
            self._monitored_variables[monitor.name] = Variable(monitor.name, monitor.address,monitor.period,monitor.enable)
        self._updateMonitorTimers()

    def _updateMonitorTimers(self):
        self._monitor_timers = {}
        for name, var in self._monitored_variables.items():
            self._monitor_timers[name] = var.period

    def _timer_tick(self):
        for name, period in self._monitor_timers.items():
            if (self._monitored_variables[name].enable):
                if (period < self._tick_period):
                    self._monitor_timers[name] = self._monitored_variables[name].period
                    ###
                    #
                    #   Request the probe reads this variable
                    #
                    ###
                    if (self._probe.connected):
                        result = self._probe.readMemory_32(self._monitored_variables[name].address)
                        self._monitored_variables[name].content = result
                        self._pubSub.send_variable_change(self._monitored_variables[name])
                else:
                    self._monitor_timers[name] -= self._tick_period
