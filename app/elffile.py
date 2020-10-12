from elftools.elf.sections import SymbolTableSection
from elftools.elf.elffile import ELFFile
import utils


def process_file(filename):
    print('Processing file:', filename)
    with open(filename, 'rb') as f:
        get_variables(f)


def get_variables(stream):
    print('High level API...')
    elffile = ELFFile(stream)

    # Just use the public methods of ELFFile to get what we need
    # Note that section names are strings.
    print('  %s sections' % elffile.num_sections())
    section = elffile.get_section_by_name('.symtab')

    if not section:
        print('  No symbol table found. Perhaps this ELF has been stripped?')
        return

    # A section type is in its header, but the name was decoded and placed in
    # a public attribute.
    print('  Section name: %s, type: %s' % (
        section.name, section['sh_type']))

    # But there's more... If this section is a symbol table section (which is
    # the case in the sample ELF file that comes with the examples), we can
    # get some more information about it.
    if isinstance(section, SymbolTableSection):
        num_symbols = section.num_symbols()
        print("  It's a symbol section with %s symbols" % num_symbols)
        for i in range(0, num_symbols):
            symbol = section.get_symbol(i)
            if symbol.name != '' and len(symbol.name) > 2:
                info = symbol.__getitem__('st_info')
                sType = info.__getitem__('type')
                if sType == 'STT_OBJECT':
                    value = symbol.entry.__getitem__('st_value')
                    if value >= 536870912:
                        print(f"  Symbol: {symbol.name} - {utils.format_hex(value, 8, False, False)}")

if __name__ == '__main__':
    process_file('F:\\DataRoot\\Projects\\ctxMonitor_Workspace\\InitialTest_1\\elf_files\\Blinky_401RE.elf')
