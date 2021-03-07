import unittest
from hamming import *


class TestHamming(unittest.TestCase):

    def test_insert_empty_control_bits(self):
        barr = bytearray.fromhex('ffffffff')
        msg_len = 32+6
        res = insert_empty_control_bits(barr,msg_len)
        target = bytearray.fromhex('2efefffefc')
        
        self.assertEqual(res, target)
    
    def test_insert_control_bits(self):
        arr = bytearray.fromhex('0000000000')
        k = 6
        bits = [1 for i in range(6)]
        insert_control_bits(arr, k, bits)

        target = bytearray.fromhex('d101000100')
        self.assertEqual(target, arr)

    def test_write_bits(self):
        src = bytearray.fromhex('000000')
        dst = bytearray.fromhex('ffff')
        write_bits(dst, src, 8, 0, 7)
        
        target = bytearray.fromhex('ff01')
        self.assertEqual(target, dst)
    
    def test_insert_err(self):
        arr = bytearray.fromhex('00')
        insert_err(arr, 3)

        target = bytearray.fromhex('10')
        self.assertEqual(arr, target)

if __name__ == '__main__':
    unittest.main()