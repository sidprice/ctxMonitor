import serial
import binascii
import utilities


class Probe:
    _OK = 'OK'

    def __init__(self, serial_instance):
        super().__init__()

        self.serial = serial_instance

    def _sendAck(self):
        self.serial.write('+'.encode())

    def _sendNak(self):
        self.serial.write('-'.encode())

    def _checkAck(self):
        ackCharacter = self.serial.read(1).decode('UTF-8')
        return ackCharacter == '+'

    def _sendPacket(self, packet):
        '''
            Send the passed packet to the probe and wait for an
            ACK.

            If a NAK is received, resend the packet
        '''
        while True:
            self.serial.write(packet.encode())
            if self._checkAck() == True:
                break

    def _calculateChecksum(self, inputString):
        asBytes = bytes(inputString, 'UTF-8')
        checksum = 0
        for byte in asBytes:
            checksum += byte
            checksum &= 0xff
        return checksum

    def sendPacket(self, packet):
        self._sendPacket(packet)

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

    def getReply(self, packet):
        '''
            Return the packet data contents.

            Assumes the caller has validated the packet
        '''
        checksumStart = packet.find('#', 1)
        if checksumStart != -1:
            return packet[1:checksumStart]
        else:
            return None

    def _readInput(self):
        '''
            Start by reading the first character from the probe. It
            should be either '$' or a '+'

            Discard the '+' characters

            If the first character is '$', read up to the '#' and two more characters.

            On sucessful reading acknowledge the packet
        '''
        result = None
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

            result = self.getReply(inputCharacters)
            if result != None:
                self._sendAck()
            else:
                self.sendNak()
        return result

    def getResponse(self):
        inputResponse = self._readInput()
        if inputResponse == None:
            return inputResponse
        if inputResponse.startswith('OK') == False:
            if inputResponse.startswith('O'):
                '''
                    The response is ASCII hex so decode it
                '''
                asbytes = bytes.fromhex(inputResponse[1:])
                inputResponse = asbytes.decode("ASCII")
        return inputResponse

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
                probe.sendCommand('s')
                while True:
                    '''
                        Loop here reading resonses until "OK" is received
                    '''
                    response = probe.getResponse()
                    if response != None:
                        if response == "OK":
                            break
                        print(response, end=' ')
                probe.sendCommand('vAttach;1', False)
                response = probe.getResponse()
                # Read memory as a test
                probe.sendCommand('m20000000,4', False)
                value = probe.getResponse()

                value = utilities.integerFromAsciiHex(value)
                result = utilities.integerToHexDisplayValue(value)
                
                print(f'Memory address 0x20000000 contains {result}')
            else:
                print('Failed to connect')
    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    main()