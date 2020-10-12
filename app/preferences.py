##########################################################################
#
#   This class provides a unified API for loading and saving preferences
#
#   NOTE:
#       This is a Singleton class, the whole application must use the
#       same instance.
#
##########################################################################

from PyQt5.QtCore import QSettings

class Preferences(QSettings):
    __instance = None
    @staticmethod
    def getInstance():
        if Preferences.__instance == None:
            Preferences()
        return Preferences.__instance

    ###
    #
    #   Preference value access strings
    #
    ##
    file_elf = 'File/elf_file'
    path_elf = 'file/open'

    def __init__(self):
        '''
            Virtually private constructor
        '''
        if Preferences.__instance != None:
            raise Exception('This class is a singleton')
        else:
            super().__init__()
            Preferences.__instance = self
    ##########
    #
    #   Preference access methods
    #
    #########

    def elf_file(self):
        return self.value(self.file_elf)
    
    def set_elf_file(self, name):
        self.setValue(self.file_elf, name)

    def remove_elf_file(self):
        self.remove(self.file_elf)

    def elf_path(self):
        return self.value(self.path_elf)
    
    def set_elf_path(self, path):
        self.setValue(self.path_elf, path)