"""Unit test for CPU.py"""

import CPU
import unittest




class TestALUFunctions(unittest.TestCase):

    def setUp(self):
        self.CPU = CPU.c6502()

    def testClearMemory(self):
        self.CPU.clear_memory()
        self.assertEqual(0, sum(self.CPU.memory))
    
    def testADC(self):
        pass
    
        

    def testCLC(self):
        self.CPU.cycles = 0
        self.CPU.PC = 0
        self.CPU.carry = 1
        
        self.CPU.memory[0] = 0x18
        self.CPU.step()
        self.assertEqual(0, self.CPU.carry)
        self.assertEqual(2, self.CPU.cycles)

    def testCLD(self):
        """"""
    """
    def testsample(self):
        self.assertRaises(ValueError, random.sample, self.seq, 20)
        for element in random.sample(self.seq, 5):
            self.assert_(element in self.seq)"""

if __name__ == '__main__':
    unittest.main()
