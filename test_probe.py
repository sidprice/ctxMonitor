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
##########################################################################

import unittest
from unittest.mock import Mock
import probe as Probe

'''
    Test class for the ctxMonitor Probe class
'''


class TestProbe(unittest.TestCase):
    ##########################################################################
    #
    #   Test packets used in this class
    #
    ##########################################################################

    _pkt8 = '$38#6B'  # 8-bit value
    _pkt16 = '$3038#CE'  # 16-bit value
    _pkt32 = '$00380240#91'  # 32-bit value
    _pkt64 = '$0038024010000000#12'  # 64-bit value

    ##########################################################################
    #
    #   Tests  "_extractReply" correctly extracts 8, 16, and 32 bit values
    #
    #   Note that the method "_extractReply" assumes the calling
    #   method has validated the packet; it does no validation of
    #   the packet.
    #
    ##########################################################################

    ##########################################################################
    #
    #   Tests:
    #       8-bit extraction - good & bad
    #
    ##########################################################################

    def test_extractReply_8bit_success(self):
        probe = Probe.Probe(None)
        self.assertEqual(probe._extractReply(self._pkt8), '38')

    def test_extractReply_8bit_fail(self):
        probe = Probe.Probe(None)
        self.assertNotEqual(probe._extractReply(self._pkt8), '00')

    ##########################################################################
    #
    #   Tests:
    #       not 8-bit input
    #
    ##########################################################################

    def test_extractReply_not_8bit(self):
        probe = Probe.Probe(None)
        self.assertNotEqual(probe._extractReply(self._pkt16), '30')
        self.assertNotEqual(probe._extractReply(self._pkt16), '38')

    ##########################################################################
    #
    #   Tests:
    #       Good and bad 16-bit packets
    #
    ##########################################################################

    def test_extractReply_16bit_success(self):
        probe = Probe.Probe(None)
        self.assertEqual(probe._extractReply(self._pkt16), '3038')

    def test_extractReply_16bit_fail(self):
        probe = Probe.Probe(None)
        self.assertNotEqual(probe._extractReply(self._pkt16), '0000')

    ##########################################################################
    #
    #   Tests:
    #       Good and bad 32-bit packets
    #
    ##########################################################################

    def test_extractReply_32bit_success(self):
        probe = Probe.Probe(None)
        self.assertEqual(probe._extractReply(self._pkt32), '00380240')

    def test_extractReply_32bit_fail(self):
        probe = Probe.Probe(None)
        self.assertNotEqual(probe._extractReply(self._pkt32), '00000000')

    ##########################################################################
    #
    #   Tests:
    #       Good and bad 64-bit packets
    #
    ##########################################################################

    def test_extractReply_64bit_success(self):
        probe = Probe.Probe(None)
        self.assertEqual(probe._extractReply(self._pkt64), '0038024010000000')

    def test_extractReply_64bit_fail(self):
        probe = Probe.Probe(None)
        self.assertNotEqual(probe._extractReply(self._pkt64), '0000000000000000')

    ##########################################################################
    #
    #   Test _readInput recieves and builds packets
    #
    ##########################################################################

    def test_readInput_good_packet(self):
        serial = Mock()
        serial.read.side_effect = [b'$', b'3', b'8', b'#', b'6', b'B']
        probe = Probe.Probe(serial)
        self.assertEqual(probe._readInput(), '38')

    def test_readInput_bad_leader(self):
        serial = Mock()
        serial.read.side_effect = [b'x', b'3', b'8', b'#', b'6', b'B']
        probe = Probe.Probe(serial)
        self.assertEqual(probe._readInput(), None)

    def test_readInput_bad_checksum(self):
        serial = Mock()
        serial.read.side_effect = [b'$', b'3', b'8', b'#', b'5', b'B']
        probe = Probe.Probe(serial)
        self.assertEqual(probe._readInput(), None)

    ##########################################################################
    #
    #   Test _checkAck
    #
    ##########################################################################

    def test_check_ack_good(self):
        serial = Mock()
        serial.read.side_effect = [b'+']
        probe = Probe.Probe(serial)
        self.assertTrue(probe._checkAck())

    def test_check_ack_fail(self):
        serial = Mock()
        serial.read.side_effect = [b'-']
        probe = Probe.Probe(serial)
        self.assertFalse(probe._checkAck())

    def testReadMemory_8(self):
        probe = Probe.Probe(None)
        probe.readMemory_8(0x20000000)

    def testReadMemory_16(self):
        probe = Probe.Probe(None)
        probe.readMemory_16(0x20000000)

    def testReadMemory_32(self):
        probe = Probe.Probe(None)
        probe.readMemory_32(0x20000000)

    def testReadMemory_64(self):
        probe = Probe.Probe(None)
        probe.readMemory_64(0x20000000)


if __name__ == '__main__':
    unittest.main()
