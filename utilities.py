def integerFromAsciiHex(asciihex):
    '''
        Convert the ASCII-HEX string parameter to
        an integer value.

        This method is specifically for converting 32-bit
        values from the ctxLink debug probe. The format is:
            zzyyxxww
        Where 'ww' is the most significant byte and 'zz'
        is the least significant

        If the input is less than the required length or
        contaions non-hex digits, return 'None'
    '''
    #
    # first correct the byte order to wwxxyyzz
    #
    value = asciihex[6:] + asciihex[4:6] + asciihex[2:4] + asciihex[:2]
    #
    # Iterate over the string of hex characters and
    # convert to integer
    #
    result = 0
    for char in value:
        result *= 16
        temp = ord(char) - 48
        result += temp
    return result

def integerToHexDisplayValue(integer):
    return hex(integer)
