def integerFromAsciiHex(asciihex):
    '''
        Convert the ASCII-HEX string parameter to
        an integer value.

        This function processes 8, 16, 32, and 64-bit strings. The
        formats are:
            8-bit                 zz
            16-bit              yyzz
            32-bit          wwxxyyzz
            64-bit  ssttuuvvwwxxyyzz
        
        This method is specifically for converting 32-bit

        Where 'ss' is the most significant byte and 'zz'
        is the least significant

        If the input is less than the required length or
        contains non-hex digits, return 'None'
    '''
    #
    # first correct the byte order to ssttuuvvwwxxyyzz
    #
    length = len(asciihex)
    if (length > 0 and length < 4):
        value = asciihex[:2]
    elif (length < 8):
        value = asciihex[2:4] + asciihex[:2]
    elif (length < 16):
        value = asciihex[6:] + asciihex[4:6] + asciihex[2:4] + asciihex[:2]
    else:
        value = asciihex[14:] + asciihex[12:14] + asciihex[10:12] + asciihex[8:10]  + asciihex[6:8] + asciihex[4:6] + asciihex[2:4] + asciihex[:2]

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

if __name__ == '__main__':
    print(integerFromAsciiHex(''))
