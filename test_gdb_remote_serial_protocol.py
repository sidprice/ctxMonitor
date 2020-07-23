import unittest
import gdb_remote_serial_protocol as gdbSrv


class TestRemoteSerialProtocol(unittest.TestCase):

    def test_validPacket(self):
        #
        #   Test the packet validation
        #
        _gdbServer = gdbSrv.GdbRemoteSerialProtocol()
        self.assertFalse(_gdbServer.validPacket(''))    # test for empty packet
        self.assertFalse(_gdbServer.validPacket('x'))  # test for leading '$'
        self.assertFalse(_gdbServer.validPacket('$OK#99'))  # checksum failure
        self.assertTrue(_gdbServer.validPacket('$OK#9A'))   # test for a valid packet

    def test_get_reply(self):
        #
        # Test the extraction of the data from the packet
        #
        _gdbServer = gdbSrv.GdbRemoteSerialProtocol()
        self.assertEqual(_gdbServer.getReply('$OK#9A'), _gdbServer._OK)

    def test_connection(self):
        pass


if __name__ == '__main__':
    unittest.main()
