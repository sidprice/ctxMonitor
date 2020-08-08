import serial
import binascii


class Probe:
    _OK = 'OK'

    def __init__(self, serial_instance):
        super().__init__()

        self.serial = serial_instance

    def _sendAck(self):
        self.serial.write('+'.encode())

    def _sendPacket(self, packet):
        self.serial.write(packet.encode())

    def _calculateChecksum(self, inputString):
        asBytes = bytes(inputString, 'UTF-8')
        checksum = 0
        for byte in asBytes:
            checksum += byte
            checksum &= 0xff
        return checksum


    #
    # A valid packet begins with a '$' and has a valid
    # checksum that is prefixed by '#'
    #
    def _validatePacket(self, packet):
        if packet.find('$', 0, 1) != -1:
            checksumStart = packet.find('#', 1)
            if checksumStart != -1:
                #
                # Calculate the 2's complement checksum of the packet starting
                # after the '$' and ending at the '#'
                #
                checksum = self._calculateChecksum(packet[1:checksumStart])
                asBytes = binascii.unhexlify(packet[checksumStart + 1:])
                inputChecksum = asBytes[0]

                if checksum == inputChecksum:
                    return True
        return False

    def _readInput(self):
        '''
            Start by reading the first character from the probe. It
            should be either '$' or a '+'

            Discard the '+' characters

            If the first character is '$', read up to the '#' and two more characters.

            On sucessful reading acknowledge the packet
        '''
        result = ''
        inputCharacters = self.serial.read(1).decode('UTF-8')
        if inputCharacters == '$':
            while True:
                lastCharacters = 2  # checksum length
                nextCharacter = self.serial.read(1).decode('UTF-8')
                inputCharacters += nextCharacter
                if nextCharacter == '#':
                    while lastCharacters != 0:
                        nextCharacter = self.serial.read(1).decode('UTF-8')
                        inputCharacters += nextCharacter
                        lastCharacters -= 1
                    break
            if self._validatePacket(inputCharacters) == True:
                self._sendAck()
                result = inputCharacters
            else:
                self.sendNak()
        return result

    def sendCommand(self, command, isMonitorCommand=True):
        '''
            This function formats and sends commands to the probe

            For "Monitor: commands the parameter "isMonitorCommand"
        must be true.
            e.g. "swdp"

            For other commands it must be false

        '''
        if isMonitorCommand == True:
            out = binascii.hexlify(bytes(command, 'UTF-8'))
            packet = f'$qRcmd,{out.decode("UTF-8")}'
        else:
            packet = f'${command}'
        checksum = self._calculateChecksum(packet[1:])
        asbytes = "{:x}".format(checksum)
        checksumString = str(asbytes)
        output = f'{packet}#{checksumString}'
        self.sendPacket(output)


    def isConnected(self):
        response = self._readInput()
        return response == self._OK


def main():
    try:
        with serial.Serial('COM8', 115200, timeout=5) as serial_instance:
            probe = Probe(serial_instance)
            if probe.isConnected() == True:
                print('connected')
                probe.sendCommand('s')
            else:
                print('Failed to connect')
    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    main()
