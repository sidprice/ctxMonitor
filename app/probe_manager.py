##########################################################################
#
#   This class manages the connection with the probe and does the 
#   variable monitoring as requested.
#
##########################################################################

from PyQt5.QtCore import QTime, QTimer

from ctx_pubsub import Ctx_PubSub
from ctx_timing import CtxTiming
from variable import Variable
from probe import Probe
from preferences import Preferences


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
    _probe = None
    
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
        #   Subscribe to variable changes
        #   
        ###
        self._pubSub = Ctx_PubSub.getInstance()
        self._pubSub.subscribe_variable_changed(self._listener_variable_changed)
        ##
        #
        #   And target power control requests
        #
        ##
        self._pubSub.subscribe_probe_target_control_power(self._listener_probe_target_power)

        self._settings = Preferences.getInstance()

    def connect_to_probe(self):
        try:
            port = self._settings.preferences_probe_port()
            if port != '':
                self._probe = Probe(port)
            else:
                pass    # TODO handle no port set up
        except:
            return  # TODO handle error
        if (self._probe.Connect()):
            print('Connected')
            if self._settings.preferences_probe_power_target() != 0:
                self._probe.powerTarget(True)
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

    def _listener_variable_changed(self, var):
        if var.monitored:
            ###
            #
            #   check if the variable is in the local database and
            #   update it if found.
            #
            #   otherwise add it
            #
            ###
            found =False
            for name, variable in self._monitored_variables.items():
                if var.name == name:
                    ###
                    #
                    #   Update the monitored variable
                    #
                    ###
                    variable.address = var.address
                    variable.period = var.period
                    variable.enable = var.enable
                    found = True
                    break
            if (found == False):
                self._monitored_variables[var.name] = var.copy()
            self._updateMonitorTimers()

    def _listener_probe_target_power(self, tpwr_enable):
        self._probe.powerTarget(tpwr_enable)

    def _updateMonitorTimers(self):
        self._monitor_timers = {}
        for name, var in self._monitored_variables.items():
            self._monitor_timers[name] = 1  # force a quick reading on any change of setting

    def _readVariable(self, variable):
        if not self._probe == None:
            if (self._probe.connected):
                result = self._probe.readMemory_32(self._monitored_variables[variable.name].address)
                self._monitored_variables[variable.name].content = result
                self._pubSub.send_variable_content_changed(self._monitored_variables[variable.name])

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
                    self._readVariable(self._monitored_variables[name])
                else:
                    self._monitor_timers[name] -= self._tick_period
