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


class VariableManager():
    __instance = None
    _pubsub = None

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

    def _listener_elf_file_load(self, elf_file):
        myVariables = Variables()
        self._symbols = myVariables.Load(elf_file)
        self._pubsub.send_variable_database(self._symbols)
    
    def _listener_elf_file_close(self):
        self._symbols = None
        self._pubsub.send_variable_database(self._symbols)


        
