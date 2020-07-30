import unittest
import gdb_remote_serial_protocol as gdbSrv
import serial


class TestRemoteSerialProtocol(unittest.TestCase):

    def _initializeSerial(self):
        serial_instance = serial.Serial('COM8', 38400, timeout=5)
        _gdbServer = gdbSrv.GdbRemoteSerialProtocol(serial_instance)
        return _gdbServer

    def test_validPacket(self):
        #
        #   Test the packet validation
        #
        _gdbServer = gdbSrv.GdbRemoteSerialProtocol(None)
        self.assertFalse(_gdbServer.validPacket(''))    # test for empty packet
        self.assertFalse(_gdbServer.validPacket('x'))  # test for leading '$'
        self.assertFalse(_gdbServer.validPacket('$OK#99'))  # checksum failure
        self.assertTrue(_gdbServer.validPacket('$OK#9A'))   # test for a valid packet

    def test_get_reply(self):
        #
        # Test the extraction of the data from the packet
        #
        _gdbServer = gdbSrv.GdbRemoteSerialProtocol(None)
        self.assertEqual(_gdbServer.getReply('$OK#9A'), _gdbServer._OK)
    #     #
    #     # The following test REQUIRES an attached BMP/ctxLink
    #     #
    # def test_connection(self):
    #     _gdbServer = self._initializeSerial()
    #     self.assertTrue(_gdbServer.connect())

    # def test_send_command(self):
    #     _gdbServer = self._initializeSerial()
    #     self.assertTrue(_gdbServer.connect())

       

if __name__ == '__main__':
    unittest.main()
