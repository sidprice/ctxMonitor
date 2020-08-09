import serial
import binascii


class GdbRemoteSerialProtocol:

    def __init__(self, serial_instance):
        super().__init__()

        self.serial = serial_instance
    _OK = 'OK'

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
    def validPacket(self, packet):
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

    def readPacket(self, skip=False):
        '''
        Data from the probe is either a Response or a Notification.

          A Response has a "$" as the first character followed by the
        data. The data is terminated with a "#" and that is followed
        by a two-character modulo 256 checksum.

          Responses must be acknowledged with a "+" (Ack) or "_" (NAK)

          Notifications are not yet implemented

        '''
        skipSecond = skip
        packet = ''
        state = 0
        while True:
            inputCharacter = self.serial.read(1).decode('UTF-8')
            if inputCharacter == "$":
                packet = inputCharacter
            elif inputCharacter == '#':
                packet += inputCharacter
                inputCharacter = self.serial.read(1).decode('UTF-8')
                packet += inputCharacter
                inputCharacter = self.serial.read(1).decode('UTF-8')
                packet += inputCharacter
                break
            elif inputCharacter == '':
                packet = ''
            else:
                if skipSecond:
                    skipSecond = False
                else:
                    packet += inputCharacter
        return packet

    def readResponse(self, skipSecond=False):
        received = self.readPacket(skipSecond)    # get Response
        received = self.getReply(received)
        asbytes = bytes.fromhex(received[1:])
        received = asbytes.decode("ASCII")
        self.sendAck()
        return received

    def sendAck(self):
        self.serial.write('+'.encode())

    def sendPacket(self, packet):
        self.serial.write(packet.encode())

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

    def signonToProbe(self):
        #
        # Send the "mon" command
        #
        self.sendCommand('s')
        #
        # Get the first block response
        #
        response = self.readResponse()
        print(response, end='')
        #
        # Get second line response
        #
        response = self.readResponse()
        print(response, end='')
        #
        # Get third line response
        #
        response = self.readResponse()
        print(response, end='')
        #
        # Get fourth line response
        #
        response = self.readResponse()
        print(response, end='')

        received = self.readPacket()
        print(received)
        #
        # send the "mon so" command (soft attach)
        #
        self.sendCommand('so')
        received = self.readPacket()
        print(received)

    def getReply(self, packet):
        '''
            Check if the passed packet is valid, if so return
        the packet data contents.

            On invalid packet return 'None'
        '''
        if self.validPacket(packet):
            if packet.find('$', 0, 1) != -1:
                checksumStart = packet.find('#', 1)
                if checksumStart != -1:
                    return packet[1:checksumStart]
            return None
        return None

    def readMemory(self, address):
        #
        # Send the command
        #
        self.serial.write('m20000000,4'.encode())
        #self.sendCommand('m20000000,4', False)
        #
        # Read reply
        #
        reply = self.readPacket(True)
        reply = self.readPacket(True)
        #
        # Send Ack
        #

        #
        # process reply
        #
        value = 0
        return value

    def connect(self):
        try:
            received = self.readPacket()
            # received = self.serial.read(6).decode('UTF-8)')
            if self.validPacket(received):
                if self.getReply(received) == self._OK:
                    self.serial.write('+'.encode())
                    return True
            return False
        except Exception as ex:
            print(ex)
            return False

    def disconnect(self):
        self.serial.close()

    def doCommands(self):
        while True:
            try:
                command = input("Enter a command for ctxLink: ")
                if command == '':
                    break
                self.serial.write((command + '\n').encode())
                while self.serial.in_waiting != 0:
                    print(self.readPacket())
                    self.sendAck()
            except:
                break

def main():
    serial_instance = serial.Serial('COM20', 38400, timeout=5)
    gdbServer = GdbRemoteSerialProtocol(serial_instance)
    if gdbServer.connect():
        gdbServer.doCommands()
        # #
        # # send the "mon" command as a test
        # #
        # gdbServer.signonToProbe()
        
        # value = gdbServer.readMemory(0x20000000)

    else:
        print('Failed to open port -> COM8')

    gdbServer.disconnect()


if __name__ == '__main__':
    main()
