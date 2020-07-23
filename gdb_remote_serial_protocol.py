import serial
import binascii


class GdbRemoteSerialProtocol:

    def __init__(self, serial_instance):
        super().__init__()

        self.serial = serial_instance
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

    def connect(self):
        try:
            received = self.serial.read(6).decode('UTF-8)')
            if self.validPacket(received):
                if self.getReply(received):
                    self.serial.write('+'.encode())
                    return True
            return False
        except Exception as ex:
            print(ex)
            return False

    def disconnect(self):
        self.serial.close()


if __name__ == '__main__':
    serial_instance = serial.Serial('COM8', 38400, timeout=5)
    gdbServer = GdbRemoteSerialProtocol(serial_instance)
    if gdbServer.connect():
        print('Probe ready!')

        gdbServer.disconnect()
    else:
        print('Failed to open port -> COM8')
