##########################################################################
#
# This class encapsulates access to the target program's global variables
#
# It loads the variable names and addresses from a give ELF file and provides
# an interface to the host program to access them.
#
##########################################################################

from elftools.elf.sections import SymbolTableSection
from elftools.elf.elffile import ELFFile
import utils

class Variables:
    def __init__(self):
        self._variables = dict({})
        self._monitored = dict({})

    #####
    #
    #   Load the variables from the passed stream
    #
    #####
    def get_variables(self, stream):
        elffile = ELFFile(stream)
        section = elffile.get_section_by_name('.symtab')

        if not section:
            return None

        if isinstance(section, SymbolTableSection):
            num_symbols = section.num_symbols()
            for i in range(0, num_symbols):
                symbol = section.get_symbol(i)
                if symbol.name != '' and len(symbol.name) > 2:
                    info = symbol.__getitem__('st_info')
                    sType = info.__getitem__('type')
                    if sType == 'STT_OBJECT':
                        value = symbol.entry.__getitem__('st_value')
                        if value >= 0x20000000:
                            self._variables[symbol.name] = utils.format_hex(value, 8, False, False)
            return self._variables
        return None

    def Load(self, filepath):
        try:
            with open(filepath, 'rb') as f:
                result = self.get_variables(f)

        except Exception:
            result = None
        return result  
    
    def get_value_by_name(self, name):
        try:
            result = self._variables[name]
        except KeyError:
            result = None
        return result


        


