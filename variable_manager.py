##########################################################################
#
#   This class loads the variable from the ELF file and serves any changes
#   in the values of monitored variables to the rest of the system
#
#   NOTE:
#       This is a Singleton class, the whole application must use the
#       same instance.
#
##########################################################################

from ctx_pubsub import Ctx_PubSub
from variables import Variables
from variable import VariableEncoder, Variable
from pathlib import Path
import json


class VariableManager():
    __instance = None
    _pubsub = None
    _symbols = dict({})
    _monitored = dict({})

    @staticmethod
    def getInstance():
        '''
            Static Access method
        '''
        if VariableManager.__instance == None:
            VariableManager()
        return VariableManager.__instance

    def __init__(self):
        '''
            Virtually private constructor
        '''
        if VariableManager.__instance != None:
            raise Exception('This class is a singleton, use getInstance')
        else:
            VariableManager.__instance = self
            self._pubsub = Ctx_PubSub.getInstance()
            #
            # Subscribe to elf file loading requests
            #
            self._pubsub.subscribe_load_elf_file(self._listener_elf_file_load)
            #
            # Subscribe to elf file close requests
            #
            self._pubsub.subscribe_close_elf_file(self._listener_elf_file_close)
            self._pubsub.subscribe_variable_changed(self._listener_variable_changed)

    def close(self):
        self._save_monitored_variables()

    def _listener_elf_file_load(self, elf_file):
        ##
        #
        #   1.  Load the set of variables from the passed ELF file
        #
        ##
        myVariables = Variables()
        self._symbols = myVariables.Load(elf_file)
        ##
        #
        #   2.  If a MON file with the same filename exists, load it and
        #           update entries in variables database
        #
        ##
        self._monitor_filepath = self._get_monitor_filename(elf_file)

        if (Path(self._monitor_filepath).exists()):
            with self._monitor_filepath.open(mode='r') as monFid:
                #
                # Load the previous session monitors
                #
                self._monitored = json.load(monFid, object_hook=Variable.decode_variable)
        ##
        #
        #   3.  If we have monitored variables make sure the entries
        #           in the variables database is updated
        #
        ##
        if (self._monitored != None):
            for name, var in self._monitored.items():
                self._symbols[name] = var.copy()
        ##
        #
        #   Publish the loaded symbols
        #
        ##
        for name, var in self._symbols.items():
            self._pubsub.send_variable_changed(var)

        self._pubsub.send_loaded_elf_file(self._symbols)

    def _get_monitor_filename(self, elf_filename):
        pathObj = Path(elf_filename)
        path = pathObj.parent
        fileName = pathObj.stem
        fileName += '.mon'
        monPath = path / fileName  # filepath for the associated "mon" file
        return monPath

    def _save_monitored_variables(self):
        with open(self._monitor_filepath, 'w') as file:
            json.dump(self._monitored, file, cls=VariableEncoder, indent=4)

    def _listener_elf_file_close(self):
        self._symbols = None
        self._pubsub.send_loaded_elf_file(self._symbols)

    def _listener_variable_changed(self, var):
        if var.monitored:
            self._monitored[var.name] = var.copy()
        else:
            if var.name in self._monitored:
                del self._monitored[var.name]

