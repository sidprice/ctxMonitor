##########################################################################
#
#   COPYRIGHT Sid Price 2022
#
#   This file is part of ctxMonitor
#
#       ctxMonitor is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License Nersion 3 as published
#   by the Free Software Foundation .
#
#       ctxMonitor is distributed in the hope that it will be useful, but WITHOUT
#   ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#   FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License along with Foobar.
#               If not, see <https://www.gnu.org/licenses/>.
#
#   Utility functions for ctxMonitor.
#
##########################################################################

def format_hex(addr, fieldsize=None, fullhex=False, lead0x=True,
                alternate=False):
    """ Format an address into a hexadecimal string.

        fieldsize:
            Size of the hexadecimal field (with leading zeros to fit the
            address into. For example with fieldsize=8, the format will
            be %08x
            If None, the minimal required field size will be used.

        fullhex:
            If True, override fieldsize to set it to the maximal size
            needed for the elfclass

        lead0x:
            If True, leading 0x is added

        alternate:
            If True, override lead0x to emulate the alternate
            hexadecimal form specified in format string with the #
            character: only non-zero values are prefixed with 0x.
            This form is used by readelf.
    """
    if alternate:
        if addr == 0:
            lead0x = False
        else:
            lead0x = True
            fieldsize -= 2

    s = '0x' if lead0x else ''
    if fullhex:
        fieldsize = 8 if self.elffile.elfclass == 32 else 16
    if fieldsize is None:
        field = '%x'
    else:
        field = '%' + '0%sx' % fieldsize
    return s + field % addr
