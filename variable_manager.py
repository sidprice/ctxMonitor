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
            raise Exception('This class is a singleton')
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
            #
            # Subscribe to monitored variables database
            #
            self._pubsub.subscribe_monitored_database(self._listener_monitored_database)

    ##########
    #
    #   1.  Load the set of variables from the passed ELF file
    #   2.  If a MON file with the same filename exists, load it to monitored
    #   3.  Update any monitored entriwes from the variables
    #
    ##########
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
        #   2.  If a MON file with the same filename exists, load it to monitored
        #
        ##
        self._monitor_filepath = self._get_monitor_filename(elf_file)
        
        if (Path(self._monitor_filepath).exists()):
            with self._monitor_filepath.open(mode='r') as monFid:
                #
                # TODO Load the previous session monitors
                #
                self._monitored = json.load(monFid, object_hook=Variable.decode_variable)

        self._pubsub.send_monitored_database(self._monitored)
        self._pubsub.send_loaded_elf_file(self._symbols)
    
    def _get_monitor_filename(self, elf_filename):
        pathObj = Path(elf_filename)
        path = pathObj.parent
        fileName = pathObj.stem
        fileName += '.mon'
        monPath = path / fileName  # filepath for the associated "mon" file
        return monPath

    def _listener_elf_file_close(self):
        self._symbols = None
        self._pubsub.send_loaded_elf_file(self._symbols)

    def _listener_monitored_database(self, monitored):
        self._monitored = monitored
        #####
        #
        #   Save the passed monitored variables list
        #
        #####
        json_string = ''
        json_string = json.dumps(self._monitored, cls=VariableEncoder, indent=4)
        with open(self._monitor_filepath, 'w') as file:
            json.dump(self._monitored, file, cls=VariableEncoder, indent=4)
