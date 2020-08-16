import unittest
import probe as Probe

'''
    Test class for the ctxMonitor Probe class
'''


class TestProbe(unittest.TestCase):
    '''
        Test packets
    '''
    _pkt8 = '$38#6B'  # 8-bit value
    _pkt16 = '$3038#CE'  # 16-bit value
    _pkt32 = '$00380240#91'  # 32-bit value
    _pkt64 = '$0038024010000000#12'  # 64-bit value

    '''
        Test that "_extractReply" correctly extracts 8, 16, and 32 bit values

        Note that the method "_extractReply" assumes the calling
        method has validated the packet; it does no validation of
        the packet.
    '''

    '''
        Tests:
            8-bit extraction - good & bad
    '''

    def test_extractReply_8bit_success(self):
        probe = Probe.Probe(None)
        self.assertEqual(probe._extractReply(self._pkt8), '38')

    def test_extractReply_8bit_fail(self):
        probe = Probe.Probe(None)
        self.assertNotEqual(probe._extractReply(self._pkt8), '00')

    '''
        Tests
            not 8-bit input
    '''

    def test_extractReply_not_8bit(self):
        probe = Probe.Probe(None)
        self.assertNotEqual(probe._extractReply(self._pkt16), '30')
        self.assertNotEqual(probe._extractReply(self._pkt16), '38')

    '''
        Tests:
            Good and bad 16-bit results
    '''

    def test_extractReply_16bit_success(self):
        probe = Probe.Probe(None)
        self.assertEqual(probe._extractReply(self._pkt16), '3038')

    def test_extractReply_16bit_fail(self):
        probe = Probe.Probe(None)
        self.assertNotEqual(probe._extractReply(self._pkt16), '0000')

    '''
        Tests:
            Good and bad 32-bit results
    '''

    def test_extractReply_32bit_success(self):
        probe = Probe.Probe(None)
        self.assertEqual(probe._extractReply(self._pkt32), '00380240')

    def test_extractReply_32bit_fail(self):
        probe = Probe.Probe(None)
        self.assertNotEqual(probe._extractReply(self._pkt32), '00000000')

    '''
        Tests:
            Good and bad 64-bit results
    '''

    def test_extractReply_64bit_success(self):
        probe = Probe.Probe(None)
        self.assertEqual(probe._extractReply(self._pkt64), '0038024010000000')

    def test_extractReply_64bit_fail(self):
        probe = Probe.Probe(None)
        self.assertNotEqual(probe._extractReply(self._pkt64), '0000000000000000')


if __name__ == '__main__':
    unittest.main()
