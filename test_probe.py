import unittest
import probe as Probe

'''
    Test class for the ctxMonitor Probe class
'''


class TestProbe(unittest.TestCase):
    '''
        Test that "_extractReply" correctly extracts 8, 16, and 32 bit values

        Note that the method "_extractReply" assumes the calling
        method has validated the packet; it does no validation of
        the packet.

        TODO Do we need 64 bit values?
    '''

    '''
        Tests:
            8-bit extraction - good & bad
    '''

    def test_extractReply_8bit_success(self):
        pkt8 = '$38#6B'  # 8-bit value
        probe = Probe.Probe(None)
        self.assertEqual(probe._extractReply(pkt8), '38')

    def test_extractReply_8bit_fail(self):
        pkt8 = '$38#6B'  # 8-bit value
        probe = Probe.Probe(None)
        self.assertNotEqual(probe._extractReply(pkt8), '00')

    '''
        Tests
            not 8-bit input
    '''

    def test_extractReply_not_8bit(self):
        pkt16 = '$3038#CE'  # 8-bit value
        probe = Probe.Probe(None)
        self.assertNotEqual(probe._extractReply(pkt16), '30')
        self.assertNotEqual(probe._extractReply(pkt16), '38')

    '''
        Tests:
            Good and bad 16-bit results
    '''
    def test_extractReply_16bit_success(self):
        pkt16 = '$3038#CE'  # 8-bit value
        probe = Probe.Probe(None)
        self.assertEqual(probe._extractReply(pkt16), '3038')

    def test_extractReply_16bit_fail(self):
        pkt16 = '$3038#CE'  # 8-bit value
        probe = Probe.Probe(None)
        self.assertNotEqual(probe._extractReply(pkt16), '0000')


if __name__ == '__main__':
    unittest.main()
