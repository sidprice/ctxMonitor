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
    edit_pref_last_tab = 'edit/preferences/last_tab'
    edit_pref_probe_port = 'edit/preferences/probe_port'
    edit_pref_probe_power_target = 'edit/preferences/probe_power_target'

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
    
    def preferences_last_tab(self):
        result = self.value(self.edit_pref_last_tab)
        if result == None:
            result = 0
        return result

    def set_preferences_last_tab(self, tab):
        self.setValue(self.edit_pref_last_tab, tab)

    def preferences_probe_port(self):
        result = self.value(self.edit_pref_probe_port)
        if result == None:
            result = ''
        return result
    
    def set_preferences_probe_port(self, port):
        self.setValue(self.edit_pref_probe_port, port)
    
    def preferences_probe_power_target(self):
        result = self.value(self.edit_pref_probe_power_target)
        if result == None:
            result = 0
        return result

    def set_preferences_probe_power_target(self, enable):
        self.setValue(self.edit_pref_probe_power_target, enable)
