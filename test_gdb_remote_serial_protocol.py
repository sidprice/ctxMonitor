import unittest
import gdb_remote_serial_protocol as gdbSrv


class TestRemoteSerialProtocol(unittest.TestCase):

    def test_validPacket(self):
        _gdbServer = gdbSrv.GdbRemoteSerialProtocol()
        self.assertTrue(_gdbServer.validPacket('$OK#9A'))

    def test_get_reply(self):
        _gdbServer = gdbSrv.GdbRemoteSerialProtocol()
        self.assertEqual(_gdbServer.getReply('$OK#9A'), 'OK')

    def test_connection(self):
        pass


if __name__ == '__main__':
    unittest.main()
