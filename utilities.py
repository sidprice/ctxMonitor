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

    startIndex = 0
    value =''
    while (length):
        value = asciihex[startIndex: startIndex + 2] + value
        startIndex += 2
        length -= 2

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
    print(hex(integerFromAsciiHex('00')))       # 2
    print(hex(integerFromAsciiHex('0038')))     # 4
    print(hex(integerFromAsciiHex('003802')))   # 6
    print(hex(integerFromAsciiHex('00380240'))) #8
    print(hex(integerFromAsciiHex('0038024010')))   #10
    print(hex(integerFromAsciiHex('003802401000'))) #12
    print(hex(integerFromAsciiHex('00380240100000')))   #14
    print(hex(integerFromAsciiHex('0038024010000000'))) #16
