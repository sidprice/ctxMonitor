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
from pathlib import Path
import json

class VariableManager():
    __instance = None
    _pubsub = None
    _symbols = None
    _monitored = None

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
        pathObj = Path(elf_file)
        path = pathObj.parent
        fileName = pathObj.stem
        fileName += '.mon'
        monPath = path / fileName  # filepath for the associated "mon" file
        
        if (Path(monPath).exists()):
            with monPath.open(mode='r') as monFid:
                #
                # Load the previous session monitors
                #
                pass

        self._pubsub.send_monitored_database(self._monitored)
        self._pubsub.send_loaded_elf_file(self._symbols)
    
    def _listener_elf_file_close(self):
        self._symbols = None
        self._pubsub.send_variable_database(self._symbols)


        
