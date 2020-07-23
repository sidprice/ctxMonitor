import serial
import binascii


class GdbRemoteSerialProtocol:
    _OK = 'OK'

    #
    # A valid packet begins with a '$' and has a valid
    # checksum that is prefixed by '#'
    #
    def validPacket(self, packet):
        if packet.find('$', 0, 1) != -1:
            checksumStart = packet.find('#', 1)
            if checksumStart != -1:
                checkSum = 0
                #
                # Calculate the 2's complement checksum of the packet starting
                # after the '$' and ending at the '#'
                #
                asBytes = bytes(packet[1:checksumStart], 'UTF-8')
                for byte in asBytes:
                    checkSum += byte

                asBytes = binascii.unhexlify(packet[checksumStart + 1:])
                inputChecksum = asBytes[0]

                if checkSum == inputChecksum:
                    return True
        return False

    def getReply(self, packet):
        if self.validPacket(packet):
            if packet.find('$', 0, 1) != -1:
                checksumStart = packet.find('#', 1)
                if checksumStart != -1:
                    return packet[1:checksumStart]
            return None
        return None

    def connect(self, port):
        try:
            with serial.Serial(port, 38400, timeout=5) as ser:
                received = ser.read(6).decode('UTF-8)')
                if self.validPacket(received):
                    if self.getReply(received):
                        ser.write('+'.encode())
                        return True
                return False
        except Exception as ex:
            print(ex)
            return False

    def disconnect(self):
        ser.close()


if __name__ == '__main__':
    gdbServer = GdbRemoteSerialProtocol()
    if gdbServer.connect('COM8'):
        print('Probe ready!')

        gdbServer.disconnect()
    else:
        print('Failed to open port -> COM8')
