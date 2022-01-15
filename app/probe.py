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
#   This class manages the probe.
#
##########################################################################
from time import sleep
import serial
import binascii
import utilities


class Probe:
    _OK = 'OK'
    connected = False

    def __init__(self, connection):
        super().__init__()

        try:
            self.serial = serial.Serial(connection, 115200, timeout=10)
        except serial.SerialException:
            raise

    def _sendAck(self):
        self.serial.write('+'.encode())

    def _sendNak(self):
        self.serial.write('-'.encode())

    def _checkAck(self):
        ackCharacter = self.serial.read(1).decode('UTF-8')
        result = True
        if ackCharacter != '+':
            result = False
        return result

    def _sendPacket(self, packet):
        '''
            Send the passed packet to the probe and wait for an
            ACK.

            If a NAK is received, resend the packet
        '''
        output = packet.encode()
        while True:  # TODO Introduce a retry/fail count
            self.serial.write(output)
            if self._checkAck() == True:
                break

    def _loopForOK(self):
        while True:
            '''
                Loop here reading resonses until "OK" is received
            '''
            response = self.getResponse()
            if response != None:
                if response == "OK":
                    break
                print(response, end=' ')

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

    def _extractReply(self, packet):
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
        if inputCharacters == '':
            print('Problem')
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

            if self._validatePacket(inputCharacters) == False:
                return None

            result = self._extractReply(inputCharacters)
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
        asbytes = "{:02x}".format(checksum)
        checksumString = str(asbytes)
        output = f'{packet}#{checksumString}'
        self.sendPacket(output)

    # TODO Is this needed and if so, is this the way to check it
    def Connect(self):
        response = self._readInput()
        self.connected = response == self._OK
        return self.connected

    def _memoryRead(self, command):
        self.sendCommand(command, False)
        value = self.getResponse()

        value = utilities.integerFromAsciiHex(value)
        result = utilities.integerToHexDisplayValue(value)
        return result

    def readMemory_8(self, address):
        command = f'm{format(address, "x")},1'
        value = self._memoryRead(command)
        print(f'Memory address {hex(address)} contains {value}')
        return value

    def readMemory_16(self, address):
        command = f'm{format(address, "x")},2'
        value = self._memoryRead(command)
        print(f'Memory address {hex(address)} contains {value}')
        return value

    def readMemory_32(self, address):
        #command = f'm{format(address, "x")},4'
        command = f'm{address},4'
        value = self._memoryRead(command)
        print(f'Memory address {address} contains {value}')
        return value

    def readMemory_64(self, address):
        command = f'm{format(address, "x")},8'
        value = self._memoryRead(command)
        print(f'Memory address {hex(address)} contains {value}')
        return value

    def powerTarget(self, enableTpwr):
        print(enableTpwr)
        if enableTpwr == True:
            command = 'enable'
        else:
            command = 'disable'

        self.sendCommand('tpwr ' + command)
        self._loopForOK()


def demo():
    try:
        probe = Probe('COM12')
        if probe.Connect() == True:
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

            # probe.readMemory_8(0x20000000)
            # probe.readMemory_16(0x20000000)
            probe.readMemory_32(0x20000000)
            # probe.readMemory_64(0x20000000)



            # Read memory as a test
            # probe.sendCommand('m20000000,4', False)
            # value = probe.getResponse()

            # value = utilities.integerFromAsciiHex(value)
            # result = utilities.integerToHexDisplayValue(value)

            # print(f'Memory address 0x20000000 contains {result}')
        else:
            print('Failed to connect')
    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    demo()
