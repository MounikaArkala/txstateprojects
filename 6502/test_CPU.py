"""Unit test for CPU.py"""

import CPU
import unittest


#~~ Helpful class to inherit from w/ common functionality ~~      
class TestCPUTemplate(unittest.TestCase):
    def setUp(self):
        self.CPU = CPU.c6502()
    
    def loadMem(self, offset, vals):
        for i in range(len(vals)):
            self.CPU.memory[offset + i] = vals[i]
    
    #OPCODE TESTS
    
    #Logical Operations - Perform logical operations on the accumulator and a value stored in memory.
    
    # Shifts - Shift the bits of either the accumulator or a memory location one bit to the left or right. 
    
    

#~~ General CPU tests ~~
class TestArithmeticFunctions(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def testUnSign(self):
        self.assertEqual(CPU.unSign(0,    8),  0)
        self.assertEqual(CPU.unSign(0x01, 8),  1)
        self.assertEqual(CPU.unSign(0xFF, 8), -1)
        self.assertEqual(CPU.unSign(0x7F, 8),  0x7F)
        self.assertEqual(CPU.unSign(0x80, 8), -128)
        self.assertEqual(CPU.unSign(0xF0, 8), -0x10)


class TestCPUFunctions(TestCPUTemplate):
    def testClearMemory(self):
        self.CPU.clear_memory()
        self.assertEqual(0, sum(self.CPU.memory))
        
    def testPS(self):
        for i in range(0x100):
            self.CPU.PS = i #test setting self.CPU.PS
            self.assertEqual(i | 0x20, self.CPU.PS) #test getting self.CPU.PS as well.


#~~ Opcode tests ~~
class TestBranchOpcodes(TestCPUTemplate):    
    #Branches
    def testBCC(self):
        #test a successful branch (bypass an X increment)
        self.CPU.reset()
        self.CPU.carry = 0
        self.loadMem(0, [0x90, 0x01, 0xE8, 0xE8, 0xC8]) #BCC(dis) INX INX INY
        self.CPU.step() #should branch
        self.CPU.step() #should increment x
        self.CPU.step() #should increment y
        self.assertEqual(self.CPU.cycles, 2+2+3) #inc + inc + successful branch
        self.assertEqual(self.CPU.X, 1)
        self.assertEqual(self.CPU.Y, 1)         
        
        #test an unsuccessful branch
        self.CPU.reset()
        self.CPU.carry = 1
        self.loadMem(0, [0x90, 0x01, 0xE8, 0xE8, 0xC8]) #BCC(dis) INX INX INY
        self.CPU.step() #shouldn't branch
        self.CPU.step() #should increment x
        self.CPU.step() #should increment x
        self.assertEqual(self.CPU.cycles, 2+2+2) #inc + inc + unsuccessful branch
        self.assertEqual(self.CPU.X, 2)
        self.assertEqual(self.CPU.Y, 0)     
        
        #test a successful branch across page boundary (cycles should be 1 higher than before.)
        self.CPU.reset()
        self.CPU.carry = 0
        self.CPU.PC = 253
        self.loadMem(253, [0x90, 0x01, 0xE8, 0xE8, 0xC8]) #BCC(dis) INX INX INY
        self.CPU.step() #should branch
        self.CPU.step() #should increment x
        self.CPU.step() #should increment y
        self.assertEqual(self.CPU.cycles, 2+2+4) #inc + inc + successful branch+page boundary.
        self.assertEqual(self.CPU.X, 1)
        self.assertEqual(self.CPU.Y, 1)
        
    
    def testBCS(self):
        #test a successful branch (bypass an X increment)
        self.CPU.reset()
        self.CPU.carry = 1
        self.loadMem(0, [0xB0, 0x01, 0xE8, 0xE8, 0xC8]) #BCC(dis) INX INX INY
        self.CPU.step() #should branch
        self.CPU.step() #should increment x
        self.CPU.step() #should increment y
        self.assertEqual(self.CPU.cycles, 2+2+3) #inc + inc + successful branch
        self.assertEqual(self.CPU.X, 1)
        self.assertEqual(self.CPU.Y, 1)         
        
        #test an unsuccessful branch
        self.CPU.reset()
        self.CPU.carry = 0
        self.loadMem(0, [0xB0, 0x01, 0xE8, 0xE8, 0xC8]) #BCC(dis) INX INX INY
        self.CPU.step() #shouldn't branch
        self.CPU.step() #should increment x
        self.CPU.step() #should increment x
        self.assertEqual(self.CPU.cycles, 2+2+2) #inc + inc + unsuccessful branch
        self.assertEqual(self.CPU.X, 2)
        self.assertEqual(self.CPU.Y, 0)     
        
        #test a successful branch across page boundary (cycles should be 1 higher than before.)
        self.CPU.reset()
        self.CPU.carry = 1
        self.CPU.PC = 253
        self.loadMem(253, [0xB0, 0x01, 0xE8, 0xE8, 0xC8]) #BCC(dis) INX INX INY
        self.CPU.step() #should branch
        self.CPU.step() #should increment x
        self.CPU.step() #should increment y
        self.assertEqual(self.CPU.cycles, 2+2+4) #inc + inc + successful branch+page boundary.
        self.assertEqual(self.CPU.X, 1)
        self.assertEqual(self.CPU.Y, 1)
        
    def testBEQ(self):
        #test a successful branch (bypass an X increment)
        self.CPU.reset()
        self.CPU.zero = 1
        self.loadMem(0, [0xF0, 0x01, 0xE8, 0xE8, 0xC8]) #BCC(dis) INX INX INY
        self.CPU.step() #should branch
        self.CPU.step() #should increment x
        self.CPU.step() #should increment y
        self.assertEqual(self.CPU.cycles, 2+2+3) #inc + inc + successful branch
        self.assertEqual(self.CPU.X, 1)
        self.assertEqual(self.CPU.Y, 1)         
        
        #test an unsuccessful branch
        self.CPU.reset()
        self.CPU.zero = 0
        self.loadMem(0, [0xF0, 0x01, 0xE8, 0xE8, 0xC8]) #BCC(dis) INX INX INY
        self.CPU.step() #shouldn't branch
        self.CPU.step() #should increment x
        self.CPU.step() #should increment x
        self.assertEqual(self.CPU.cycles, 2+2+2) #inc + inc + unsuccessful branch
        self.assertEqual(self.CPU.X, 2)
        self.assertEqual(self.CPU.Y, 0)     
        
        #test a successful branch across page boundary (cycles should be 1 higher than before.)
        self.CPU.reset()
        self.CPU.zero = 1
        self.CPU.PC = 253
        self.loadMem(253, [0xF0, 0x01, 0xE8, 0xE8, 0xC8]) #BCC(dis) INX INX INY
        self.CPU.step() #should branch
        self.CPU.step() #should increment x
        self.CPU.step() #should increment y
        self.assertEqual(self.CPU.cycles, 2+2+4) #inc + inc + successful branch+page boundary.
        self.assertEqual(self.CPU.X, 1)
        self.assertEqual(self.CPU.Y, 1)
        
    def testBMI(self):
        #test a successful branch (bypass an X increment)
        self.CPU.reset()
        self.CPU.negative = 1
        self.loadMem(0, [0x30, 0x01, 0xE8, 0xE8, 0xC8]) #BCC(dis) INX INX INY
        self.CPU.step() #should branch
        self.CPU.step() #should increment x
        self.CPU.step() #should increment y
        self.assertEqual(self.CPU.cycles, 2+2+3) #inc + inc + successful branch
        self.assertEqual(self.CPU.X, 1)
        self.assertEqual(self.CPU.Y, 1)         
        
        #test an unsuccessful branch
        self.CPU.reset()
        self.CPU.negative = 0
        self.loadMem(0, [0x30, 0x01, 0xE8, 0xE8, 0xC8]) #BCC(dis) INX INX INY
        self.CPU.step() #shouldn't branch
        self.CPU.step() #should increment x
        self.CPU.step() #should increment x
        self.assertEqual(self.CPU.cycles, 2+2+2) #inc + inc + unsuccessful branch
        self.assertEqual(self.CPU.X, 2)
        self.assertEqual(self.CPU.Y, 0)     
        
        #test a successful branch across page boundary (cycles should be 1 higher than before.)
        self.CPU.reset()
        self.CPU.negative = 1
        self.CPU.PC = 253
        self.loadMem(253, [0x30, 0x01, 0xE8, 0xE8, 0xC8]) #BCC(dis) INX INX INY
        self.CPU.step() #should branch
        self.CPU.step() #should increment x
        self.CPU.step() #should increment y
        self.assertEqual(self.CPU.cycles, 2+2+4) #inc + inc + successful branch+page boundary.
        self.assertEqual(self.CPU.X, 1)
        self.assertEqual(self.CPU.Y, 1)
        
    def testBNE(self):
        #test a successful branch (bypass an X increment)
        self.CPU.reset()
        self.CPU.zero = 0
        self.loadMem(0, [0xD0, 0x01, 0xE8, 0xE8, 0xC8]) #BCC(dis) INX INX INY
        self.CPU.step() #should branch
        self.CPU.step() #should increment x
        self.CPU.step() #should increment y
        self.assertEqual(self.CPU.cycles, 2+2+3) #inc + inc + successful branch
        self.assertEqual(self.CPU.X, 1)
        self.assertEqual(self.CPU.Y, 1)         
        
        #test an unsuccessful branch
        self.CPU.reset()
        self.CPU.zero = 1
        self.loadMem(0, [0xD0, 0x01, 0xE8, 0xE8, 0xC8]) #BCC(dis) INX INX INY
        self.CPU.step() #shouldn't branch
        self.CPU.step() #should increment x
        self.CPU.step() #should increment x
        self.assertEqual(self.CPU.cycles, 2+2+2) #inc + inc + unsuccessful branch
        self.assertEqual(self.CPU.X, 2)
        self.assertEqual(self.CPU.Y, 0)     
        
        #test a successful branch across page boundary (cycles should be 1 higher than before.)
        self.CPU.reset()
        self.CPU.zero = 0
        self.CPU.PC = 253
        self.loadMem(253, [0xD0, 0x01, 0xE8, 0xE8, 0xC8]) #BCC(dis) INX INX INY
        self.CPU.step() #should branch
        self.CPU.step() #should increment x
        self.CPU.step() #should increment y
        self.assertEqual(self.CPU.cycles, 2+2+4) #inc + inc + successful branch+page boundary.
        self.assertEqual(self.CPU.X, 1)
        self.assertEqual(self.CPU.Y, 1)
        
    def testBPL(self):
        #test a successful branch (bypass an X increment)
        self.CPU.reset()
        self.CPU.negative = 0
        self.loadMem(0, [0x10, 0x01, 0xE8, 0xE8, 0xC8]) #BCC(dis) INX INX INY
        self.CPU.step() #should branch
        self.CPU.step() #should increment x
        self.CPU.step() #should increment y
        self.assertEqual(self.CPU.cycles, 2+2+3) #inc + inc + successful branch
        self.assertEqual(self.CPU.X, 1)
        self.assertEqual(self.CPU.Y, 1)         
        
        #test an unsuccessful branch
        self.CPU.reset()
        self.CPU.negative = 1
        self.loadMem(0, [0x10, 0x01, 0xE8, 0xE8, 0xC8]) #BCC(dis) INX INX INY
        self.CPU.step() #shouldn't branch
        self.CPU.step() #should increment x
        self.CPU.step() #should increment x
        self.assertEqual(self.CPU.cycles, 2+2+2) #inc + inc + unsuccessful branch
        self.assertEqual(self.CPU.X, 2)
        self.assertEqual(self.CPU.Y, 0)     
        
        #test a successful branch across page boundary (cycles should be 1 higher than before.)
        self.CPU.reset()
        self.CPU.negative = 0
        self.CPU.PC = 253
        self.loadMem(253, [0x10, 0x01, 0xE8, 0xE8, 0xC8]) #BCC(dis) INX INX INY
        self.CPU.step() #should branch
        self.CPU.step() #should increment x
        self.CPU.step() #should increment y
        self.assertEqual(self.CPU.cycles, 2+2+4) #inc + inc + successful branch+page boundary.
        self.assertEqual(self.CPU.X, 1)
        self.assertEqual(self.CPU.Y, 1)
        
    def testBVC(self):
        #test a successful branch (bypass an X increment)
        self.CPU.reset()
        self.CPU.overflow = 0
        self.loadMem(0, [0x50, 0x01, 0xE8, 0xE8, 0xC8]) #BCC(dis) INX INX INY
        self.CPU.step() #should branch
        self.CPU.step() #should increment x
        self.CPU.step() #should increment y
        self.assertEqual(self.CPU.cycles, 2+2+3) #inc + inc + successful branch
        self.assertEqual(self.CPU.X, 1)
        self.assertEqual(self.CPU.Y, 1)         
        
        #test an unsuccessful branch
        self.CPU.reset()
        self.CPU.overflow = 1
        self.loadMem(0, [0x50, 0x01, 0xE8, 0xE8, 0xC8]) #BCC(dis) INX INX INY
        self.CPU.step() #shouldn't branch
        self.CPU.step() #should increment x
        self.CPU.step() #should increment x
        self.assertEqual(self.CPU.cycles, 2+2+2) #inc + inc + unsuccessful branch
        self.assertEqual(self.CPU.X, 2)
        self.assertEqual(self.CPU.Y, 0)     
        
        #test a successful branch across page boundary (cycles should be 1 higher than before.)
        self.CPU.reset()
        self.CPU.overflow = 0
        self.CPU.PC = 253
        self.loadMem(253, [0x50, 0x01, 0xE8, 0xE8, 0xC8]) #BCC(dis) INX INX INY
        self.CPU.step() #should branch
        self.CPU.step() #should increment x
        self.CPU.step() #should increment y
        self.assertEqual(self.CPU.cycles, 2+2+4) #inc + inc + successful branch+page boundary.
        self.assertEqual(self.CPU.X, 1)
        self.assertEqual(self.CPU.Y, 1)
        
    def testBVS(self):
        #test a successful branch (bypass an X increment)
        self.CPU.reset()
        self.CPU.overflow = 1
        self.loadMem(0, [0x70, 0x01, 0xE8, 0xE8, 0xC8]) #BCC(dis) INX INX INY
        self.CPU.step() #should branch
        self.CPU.step() #should increment x
        self.CPU.step() #should increment y
        self.assertEqual(self.CPU.cycles, 2+2+3) #inc + inc + successful branch
        self.assertEqual(self.CPU.X, 1)
        self.assertEqual(self.CPU.Y, 1)         
        
        #test an unsuccessful branch
        self.CPU.reset()
        self.CPU.overflow = 0
        self.loadMem(0, [0x70, 0x01, 0xE8, 0xE8, 0xC8]) #BCC(dis) INX INX INY
        self.CPU.step() #shouldn't branch
        self.CPU.step() #should increment x
        self.CPU.step() #should increment x
        self.assertEqual(self.CPU.cycles, 2+2+2) #inc + inc + unsuccessful branch
        self.assertEqual(self.CPU.X, 2)
        self.assertEqual(self.CPU.Y, 0)     
        
        #test a successful branch across page boundary (cycles should be 1 higher than before.)
        self.CPU.reset()
        self.CPU.overflow = 1
        self.CPU.PC = 253
        self.loadMem(253, [0x70, 0x01, 0xE8, 0xE8, 0xC8]) #BCC(dis) INX INX INY
        self.CPU.step() #should branch
        self.CPU.step() #should increment x
        self.CPU.step() #should increment y
        self.assertEqual(self.CPU.cycles, 2+2+4) #inc + inc + successful branch+page boundary.
        self.assertEqual(self.CPU.X, 1)
        self.assertEqual(self.CPU.Y, 1)
        
           
class TestArithmeticOpcodes(TestCPUTemplate):    
    #Arithmetic Operations - Perform arithmetic operations on registers and memory. 
    def testADC(self):        
        #test w/o carry, two positives not overflowing.
        self.CPU.reset()
        self.CPU.carry = 0
        self.CPU.A = 0x0A
        self.CPU.memory[0] = 0x69 #ADC IMM
        self.CPU.memory[1] = 0x0C
        self.CPU.step()
        self.assertEqual(self.CPU.A, 0x16)
        self.assertEqual(self.CPU.carry, 0)
        self.assertEqual(self.CPU.negative, 0)
        self.assertEqual(self.CPU.overflow, 0)
        self.assertEqual(self.CPU.cycles, 2)
        
        #test with carry, two positives not overflowing.
        self.CPU.reset()
        self.CPU.carry = 1
        self.CPU.A = 0x0A
        self.CPU.memory[0] = 0x69 #ADC IMM
        self.CPU.memory[1] = 0x0C
        self.CPU.step()
        self.assertEqual(self.CPU.A, 0x17)
        self.assertEqual(self.CPU.carry, 0)
        self.assertEqual(self.CPU.negative, 0)
        self.assertEqual(self.CPU.overflow, 0)
        self.assertEqual(self.CPU.cycles, 2)
        
        #test w/o carry, two negatives not overflowing.
        self.CPU.reset()
        self.CPU.carry = 0
        self.CPU.A = 0xE6 #-26
        self.CPU.memory[0] = 0x69 #ADC IMM
        self.CPU.memory[1] = 0xE6 #-26
        self.CPU.step()
        self.assertEqual(self.CPU.A, 0xCC)
        self.assertEqual(self.CPU.carry, 1)
        self.assertEqual(self.CPU.negative, 1)
        self.assertEqual(self.CPU.overflow, 0)
        self.assertEqual(self.CPU.cycles, 2)
        
        #test with carry, two negatives not overflowing.
        self.CPU.reset()
        self.CPU.carry = 1
        self.CPU.A = 0xE6 #-26
        self.CPU.memory[0] = 0x69 #ADC IMM
        self.CPU.memory[1] = 0xE6 #-26
        self.CPU.step()
        self.assertEqual(self.CPU.A, 0xCD)
        self.assertEqual(self.CPU.carry, 1)
        self.assertEqual(self.CPU.negative, 1)
        self.assertEqual(self.CPU.overflow, 0)
        self.assertEqual(self.CPU.cycles, 2)
        
        #test w/o carry, two positives overflowing.
        self.CPU.reset()
        self.CPU.carry = 0
        self.CPU.A = 0x3A
        self.CPU.memory[0] = 0x69 #ADC IMM
        self.CPU.memory[1] = 0x7C
        self.CPU.step()
        self.assertEqual(self.CPU.A, 0xB6)
        self.assertEqual(self.CPU.carry, 0)
        self.assertEqual(self.CPU.negative, 1)
        self.assertEqual(self.CPU.overflow, 1)
        self.assertEqual(self.CPU.cycles, 2)
        
        #test with carry, two positives overflowing.
        self.CPU.reset()
        self.CPU.carry = 1
        self.CPU.A = 0x3A
        self.CPU.memory[0] = 0x69 #ADC IMM
        self.CPU.memory[1] = 0x7C
        self.CPU.step()
        self.assertEqual(self.CPU.A, 0xB7) #B7 is negative, but it should be a positive result.
        self.assertEqual(self.CPU.carry, 0)
        self.assertEqual(self.CPU.negative, 1)
        self.assertEqual(self.CPU.overflow, 1)
        self.assertEqual(self.CPU.cycles, 2)
        
        #test w/o carry, two negatives overflowing.
        self.CPU.reset()
        self.CPU.carry = 0
        self.CPU.A = 0x9C #-100
        self.CPU.memory[0] = 0x69 #ADC IMM
        self.CPU.memory[1] = 0x9C
        self.CPU.step()
        self.assertEqual(self.CPU.A, 0x38)
        self.assertEqual(self.CPU.carry, 1)
        self.assertEqual(self.CPU.negative, 0)
        self.assertEqual(self.CPU.overflow, 1)
        self.assertEqual(self.CPU.cycles, 2)
        
        #test with carry, two negatives overflowing.
        self.CPU.reset()
        self.CPU.carry = 1
        self.CPU.A = 0x9C #-100
        self.CPU.memory[0] = 0x69 #ADC IMM
        self.CPU.memory[1] = 0x9C
        self.CPU.step()
        self.assertEqual(self.CPU.A, 0x39)
        self.assertEqual(self.CPU.carry, 1)
        self.assertEqual(self.CPU.negative, 0)
        self.assertEqual(self.CPU.overflow, 1)
        self.assertEqual(self.CPU.cycles, 2)
        
        #with carry, almost positive overflow.
        self.CPU.reset()
        self.CPU.carry = 1
        self.CPU.A = 0x64 #100
        self.CPU.memory[0] = 0x69 #ADC IMM
        self.CPU.memory[1] = 0x1A #26
        self.CPU.step()
        self.assertEqual(self.CPU.A, 0x7F)
        self.assertEqual(self.CPU.carry, 0)
        self.assertEqual(self.CPU.negative, 0)
        self.assertEqual(self.CPU.overflow, 0)
        self.assertEqual(self.CPU.cycles, 2)
        
        
        #with carry, almost negative overflow. 
        self.CPU.reset()
        self.CPU.carry = 1
        self.CPU.A = 0x9C #-100
        self.CPU.memory[0] = 0x69 #ADC IMM
        self.CPU.memory[1] = 0xE3 #-29
        self.CPU.step()
        self.assertEqual(self.CPU.A, 0x80)
        self.assertEqual(self.CPU.carry, 1)
        self.assertEqual(self.CPU.negative, 1)
        self.assertEqual(self.CPU.overflow, 0) 
        self.assertEqual(self.CPU.cycles, 2)

    def testSBC(self):
        pass
class TestRegisterTransferOpcodes(TestCPUTemplate):
    #Register Transfer Operations - Copy contents of X or Y register to the accumulator or copy contents of accumulator to X or Y register. 
    def testTAX(self):
        self.CPU.reset()
        self.CPU.A = 0xF8
        self.CPU.memory[0] = 0xAA
        self.CPU.step()
        self.assertEqual(self.CPU.A, 0xF8)
        self.assertEqual(self.CPU.X, 0xF8)
        self.assertEqual(self.CPU.negative, 1)
        self.assertEqual(self.CPU.zero, 0)
        self.assertEqual(self.CPU.cycles, 2)
        
        self.CPU.reset()
        self.CPU.A = 0x0
        self.CPU.memory[0] = 0xAA
        self.CPU.step()
        self.assertEqual(self.CPU.A, 0x0)
        self.assertEqual(self.CPU.X, 0x0)
        self.assertEqual(self.CPU.negative, 0)
        self.assertEqual(self.CPU.zero, 1)
        self.assertEqual(self.CPU.cycles, 2)
        
    def testTAY(self):
        self.CPU.reset()
        self.CPU.A = 0xF8
        self.CPU.memory[0] = 0xA8
        self.CPU.step()
        self.assertEqual(self.CPU.A, 0xF8)
        self.assertEqual(self.CPU.Y, 0xF8)
        self.assertEqual(self.CPU.negative, 1)
        self.assertEqual(self.CPU.zero, 0)
        self.assertEqual(self.CPU.cycles, 2)
        
        self.CPU.reset()
        self.CPU.A = 0x0
        self.CPU.memory[0] = 0xA8
        self.CPU.step()
        self.assertEqual(self.CPU.A, 0x0)
        self.assertEqual(self.CPU.Y, 0x0)
        self.assertEqual(self.CPU.negative, 0)
        self.assertEqual(self.CPU.zero, 1)
        self.assertEqual(self.CPU.cycles, 2)
        
    def testTSX(self):
        self.CPU.reset()
        self.CPU.S = 0xF8
        self.CPU.memory[0] = 0xBA
        self.CPU.step()
        self.assertEqual(self.CPU.X, 0xF8)
        self.assertEqual(self.CPU.S, 0xF8)
        self.assertEqual(self.CPU.negative, 1)
        self.assertEqual(self.CPU.zero, 0)
        self.assertEqual(self.CPU.cycles, 2)
        
        self.CPU.reset()
        self.CPU.S = 0x0
        self.CPU.memory[0] = 0xBA
        self.CPU.step()
        self.assertEqual(self.CPU.X, 0x0)
        self.assertEqual(self.CPU.S, 0x0)
        self.assertEqual(self.CPU.negative, 0)
        self.assertEqual(self.CPU.zero, 1)
        self.assertEqual(self.CPU.cycles, 2)
        
    def testTXS(self):
        self.CPU.reset()
        self.CPU.X = 0xF8
        self.CPU.memory[0] = 0x9A
        self.CPU.step()
        self.assertEqual(self.CPU.X, 0xF8)
        self.assertEqual(self.CPU.S, 0xF8)
        self.assertEqual(self.CPU.cycles, 2)
        
    def testTXA(self):
        self.CPU.reset()
        self.CPU.X = 0xF8
        self.CPU.memory[0] = 0x8A
        self.CPU.step()
        self.assertEqual(self.CPU.A, 0xF8)
        self.assertEqual(self.CPU.X, 0xF8)
        self.assertEqual(self.CPU.negative, 1)
        self.assertEqual(self.CPU.zero, 0)
        self.assertEqual(self.CPU.cycles, 2)
        
        self.CPU.reset()
        self.CPU.X = 0x0
        self.CPU.memory[0] = 0x8A
        self.CPU.step()
        self.assertEqual(self.CPU.A, 0x0)
        self.assertEqual(self.CPU.X, 0x0)
        self.assertEqual(self.CPU.negative, 0)
        self.assertEqual(self.CPU.zero, 1)
        self.assertEqual(self.CPU.cycles, 2)
        
        
    def testTYA(self):
        self.CPU.reset()
        self.CPU.Y = 0xF8
        self.CPU.memory[0] = 0x98
        self.CPU.step()
        self.assertEqual(self.CPU.A, 0xF8)
        self.assertEqual(self.CPU.Y, 0xF8)
        self.assertEqual(self.CPU.negative, 1)
        self.assertEqual(self.CPU.zero, 0)
        self.assertEqual(self.CPU.cycles, 2)
        
        self.CPU.reset()
        self.CPU.Y = 0x0
        self.CPU.memory[0] = 0x98
        self.CPU.step()
        self.assertEqual(self.CPU.A, 0x0)
        self.assertEqual(self.CPU.Y, 0x0)
        self.assertEqual(self.CPU.negative, 0)
        self.assertEqual(self.CPU.zero, 1)
        self.assertEqual(self.CPU.cycles, 2)
    
    
class TestStackOpcodes(TestCPUTemplate):
    #Stack Operations - Push or pull the stack or manipulate stack pointer using X register. 
    def testPHA(self):
        self.CPU.reset()
        self.CPU.A = 0xAD
        self.CPU.memory[0] = 0x48
        self.CPU.step()
        self.assertEqual(self.CPU.A, 0xAD)
        self.assertEqual(self.CPU.PS, 0 | 0x20)
        self.assertEqual(self.CPU.cycles, 3)
        self.assertEqual(self.CPU.S, 254)
        self.assertEqual(self.CPU.memory[511], 0xAD)
        
    def testPHP(self):
        self.CPU.reset()
        self.CPU.PS = 0x0F
        self.CPU.memory[0] = 0x08
        self.CPU.step()
        self.assertEqual(self.CPU.A, 0)
        self.assertEqual(self.CPU.PS, 0x0F | 0x20)
        self.assertEqual(self.CPU.S, 254)
        self.assertEqual(self.CPU.cycles, 3)
        self.assertEqual(self.CPU.memory[511], 0x0F | 0x20)
        
    def testPLA(self):
        self.CPU.reset()
        #push 0xA8 onto stack
        self.CPU.A = 0xA8
        self.CPU.memory[0] = 0x48
        self.CPU.step()
        
        self.CPU.A = 0
        #pop 0x48 into accumulator
        self.CPU.memory[1] = 0x68
        self.CPU.step()
        self.assertEqual(self.CPU.A, 0xA8)
        self.assertEqual(self.CPU.cycles, 7)
        self.assertEqual(self.CPU.negative, 1)
        self.assertEqual(self.CPU.S, 255)
        self.assertEqual(self.CPU.zero, 0) # make sure this doesn't get set.
        
        #now try zero.
        #push 0xA8 onto stack
        self.CPU.A = 0x0
        self.CPU.memory[2] = 0x48
        self.CPU.step()
        
        self.CPU.A = 0x38
        #pop 0x0 into accumulator
        self.CPU.memory[3] = 0x68
        self.CPU.step()
        self.assertEqual(self.CPU.A, 0x0)
        self.assertEqual(self.CPU.cycles, 14)
        self.assertEqual(self.CPU.negative, 0)
        self.assertEqual(self.CPU.S, 255)
        self.assertEqual(self.CPU.zero, 1)
        
    def testPLP(self):
        self.CPU.reset()
        #push 0xFF onto stack
        self.CPU.A = 0xFF
        self.CPU.memory[0] = 0x48
        self.CPU.step()
        
        self.CPU.A = 0
        #pop 0xFF into PS
        self.CPU.memory[1] = 0x28
        self.CPU.step()
        self.assertEqual(self.CPU.A, 0x0)
        self.assertEqual(self.CPU.cycles, 7)
        self.assertEqual(self.CPU.S, 255)
        self.assertEqual(self.CPU.PS, 0xFF)
    
    
class TestAddressingModes(TestCPUTemplate):
    """Note - uses ADC so all ADC instructions must be implemented!"""
    def testAllModes(self):    
        #Use ADC to make sure addressing modes work.
        
        #ABSOLUTE
        self.CPU.reset()
        self.CPU.carry = 1
        self.CPU.A = 0x9C #-100
        self.CPU.memory[0] = 0x6D #ADC ABS
        self.CPU.memory[1] = 0x52
        self.CPU.memory[2] = 0x45
        self.CPU.memory[0x4552] = 0xE3 #-29
        self.CPU.step()
        self.assertEqual(self.CPU.A, 0x80)
        self.assertEqual(self.CPU.carry, 1)
        self.assertEqual(self.CPU.negative, 1)
        self.assertEqual(self.CPU.overflow, 0) 
        self.assertEqual(self.CPU.cycles, 4)
        
        #ZERO-PAGE
        self.CPU.reset()
        self.CPU.carry = 1
        self.CPU.A = 0x9C #-100
        self.CPU.memory[0] = 0x65 #ADC ZPG
        self.CPU.memory[1] = 0x52
        self.CPU.memory[0x52] = 0xE3 #-29
        self.CPU.step()
        self.assertEqual(self.CPU.A, 0x80)
        self.assertEqual(self.CPU.carry, 1)
        self.assertEqual(self.CPU.negative, 1)
        self.assertEqual(self.CPU.overflow, 0) 
        self.assertEqual(self.CPU.cycles, 3)
             
        
        #ABSOLUTE, X  (not crossing page boundary)
        self.CPU.reset()
        self.CPU.carry = 1
        self.CPU.X = 0x03
        self.CPU.A = 0x9C #-100
        self.CPU.memory[0] = 0x7D #ADC ABX
        self.CPU.memory[1] = 0x52
        self.CPU.memory[2] = 0x00
        self.CPU.memory[0x0055] = 0xE3 #-29
        self.CPU.step()
        self.assertEqual(self.CPU.A, 0x80)
        self.assertEqual(self.CPU.carry, 1)
        self.assertEqual(self.CPU.negative, 1)
        self.assertEqual(self.CPU.overflow, 0) 
        self.assertEqual(self.CPU.cycles, 4)
        
        #ABSOLUTE, X (crossing page boundary)
        self.CPU.reset()
        self.CPU.carry = 1
        self.CPU.X = 0x03
        self.CPU.A = 0x9C #-100
        self.CPU.memory[0] = 0x7D #ADC ABX
        self.CPU.memory[1] = 0x52
        self.CPU.memory[2] = 0x01
        self.CPU.memory[0x0155] = 0xE3 #-29
        self.CPU.step()
        self.assertEqual(self.CPU.A, 0x80)
        self.assertEqual(self.CPU.carry, 1)
        self.assertEqual(self.CPU.negative, 1)
        self.assertEqual(self.CPU.overflow, 0) 
        self.assertEqual(self.CPU.cycles, 5)
        
        #ABSOLUTE, Y (not crossing page boundary)
        self.CPU.reset()
        self.CPU.carry = 1
        self.CPU.Y = 0x05
        self.CPU.A = 0x9C #-100
        self.CPU.memory[0] = 0x79 #ADC ABX
        self.CPU.memory[1] = 0x52
        self.CPU.memory[2] = 0x00
        self.CPU.memory[0x0057] = 0xE3 #-29
        self.CPU.step()
        self.assertEqual(self.CPU.A, 0x80)
        self.assertEqual(self.CPU.carry, 1)
        self.assertEqual(self.CPU.negative, 1)
        self.assertEqual(self.CPU.overflow, 0) 
        self.assertEqual(self.CPU.cycles, 4)
        
        #ABSOLUTE, Y (crossing page boundary)
        
        self.CPU.reset()
        self.CPU.carry = 1
        self.CPU.Y = 0x05
        self.CPU.A = 0x9C #-100
        self.CPU.memory[0] = 0x79 #ADC ABX
        self.CPU.memory[1] = 0x52
        self.CPU.memory[2] = 0x01
        self.CPU.memory[0x0157] = 0xE3 #-29
        self.CPU.step()
        self.assertEqual(self.CPU.A, 0x80)
        self.assertEqual(self.CPU.carry, 1)
        self.assertEqual(self.CPU.negative, 1)
        self.assertEqual(self.CPU.overflow, 0) 
        self.assertEqual(self.CPU.cycles, 5)
        
      
        #(INDIRECT, X)
        self.CPU.reset()
        self.CPU.carry = 1
        self.CPU.X = 0x52
        self.CPU.A = 0x9C #-100
        self.CPU.memory[0] = 0x61 #ADC IDX
        self.CPU.memory[1] = 0x05
        self.CPU.memory[0x0057] = 0x75 #L of 16-bit address
        self.CPU.memory[0x0058] = 0x01 #H of 16-bit address
        self.CPU.memory[0x0175] = 0xE3 #-29
        self.CPU.step()
        self.assertEqual(self.CPU.A, 0x80)
        self.assertEqual(self.CPU.carry, 1)
        self.assertEqual(self.CPU.negative, 1)
        self.assertEqual(self.CPU.overflow, 0) 
        self.assertEqual(self.CPU.cycles, 6)
        
        """
        #(INDIRECT, Y) not crossing page boundary        
        self.CPU.reset()
        self.CPU.carry = 1
        self.CPU.Y = 0x05
        self.CPU.A = 0x9C #-100
        self.CPU.memory[0] = 0x71 #ADC IDY
        self.CPU.memory[1] = 0x52
        self.CPU.memory[2] = 0x01
        self.CPU.memory[0x0157] = 0xE3 #-29
        self.CPU.step()
        self.assertEqual(self.CPU.A, 0x80)
        self.assertEqual(self.CPU.carry, 1)
        self.assertEqual(self.CPU.negative, 1)
        self.assertEqual(self.CPU.overflow, 0) 
        self.assertEqual(self.CPU.cycles, 5)
        
        #(INDIRECT, Y)  crossing page boundary     
        
        #ZERO-PAGE, X        
        self.CPU.reset()
        self.CPU.carry = 1
        self.CPU.Y = 0x05
        self.CPU.A = 0x9C #-100
        self.CPU.memory[0] = 0x79 #ADC ZPX
        self.CPU.memory[1] = 0x52
        self.CPU.memory[2] = 0x01
        self.CPU.memory[0x0157] = 0xE3 #-29
        self.CPU.step()
        self.assertEqual(self.CPU.A, 0x80)
        self.assertEqual(self.CPU.carry, 1)
        self.assertEqual(self.CPU.negative, 1)
        self.assertEqual(self.CPU.overflow, 0) 
        self.assertEqual(self.CPU.cycles, 4)
        """
        
class TestIncrementDecrementOpcodes(TestCPUTemplate):
    #Increments / Decrements - Increment or decrement the X or Y registers or a value stored in memory. 
    def testINC(self):
        pass
        
    def testDEC(self):
        pass
        
    def testINX(self):
        #check at 0
        self.CPU.reset()
        self.CPU.X = 0
        self.CPU.memory[0] = 0xE8
        self.CPU.step()
        self.assertEqual(self.CPU.X, 1)
        self.assertEqual(self.CPU.negative, 0)
        self.assertEqual(self.CPU.zero, 0)
        self.assertEqual(self.CPU.cycles, 2)
        
        #check a negative number
        self.CPU.reset()
        self.CPU.X = 0x7F
        self.CPU.memory[0] = 0xE8
        self.CPU.step()
        self.assertEqual(self.CPU.X, 0x80)
        self.assertEqual(self.CPU.negative, 1)
        self.assertEqual(self.CPU.zero, 0)
        self.assertEqual(self.CPU.cycles, 2)
        
        #check wraparound
        self.CPU.reset()
        self.CPU.X = 255
        self.CPU.memory[0] = 0xE8
        self.CPU.step()
        self.assertEqual(self.CPU.X, 0)
        self.assertEqual(self.CPU.negative, 0)
        self.assertEqual(self.CPU.zero, 1)
        self.assertEqual(self.CPU.cycles, 2)
        
    def testINY(self):
        #check at 0
        self.CPU.reset()
        self.CPU.Y = 0
        self.CPU.memory[0] = 0xC8
        self.CPU.step()
        self.assertEqual(self.CPU.Y, 1)
        self.assertEqual(self.CPU.negative, 0)
        self.assertEqual(self.CPU.zero, 0)
        self.assertEqual(self.CPU.cycles, 2)
        
        #check a negative number
        self.CPU.reset()
        self.CPU.Y = 0x7F
        self.CPU.memory[0] = 0xC8
        self.CPU.step()
        self.assertEqual(self.CPU.Y, 0x80)
        self.assertEqual(self.CPU.negative, 1)
        self.assertEqual(self.CPU.zero, 0)
        self.assertEqual(self.CPU.cycles, 2)
        
        #check wraparound
        self.CPU.reset()
        self.CPU.Y = 255
        self.CPU.memory[0] = 0xC8
        self.CPU.step()
        self.assertEqual(self.CPU.Y, 0)
        self.assertEqual(self.CPU.negative, 0)
        self.assertEqual(self.CPU.zero, 1)
        self.assertEqual(self.CPU.cycles, 2)
     
    def testDEX(self):
        #check at 1
        self.CPU.reset()
        self.CPU.X = 1
        self.CPU.memory[0] = 0xCA
        self.CPU.step()
        self.assertEqual(self.CPU.X, 0)
        self.assertEqual(self.CPU.negative, 0)
        self.assertEqual(self.CPU.zero, 1)
        self.assertEqual(self.CPU.cycles, 2)
        
        #check a negative number
        self.CPU.reset()
        self.CPU.X = 0xFF
        self.CPU.memory[0] = 0xCA
        self.CPU.step()
        self.assertEqual(self.CPU.X, 0xFE)
        self.assertEqual(self.CPU.negative, 1)
        self.assertEqual(self.CPU.zero, 0)
        self.assertEqual(self.CPU.cycles, 2)
        
        #check wraparound
        self.CPU.reset()
        self.CPU.X = 0
        self.CPU.memory[0] = 0xCA
        self.CPU.step()
        self.assertEqual(self.CPU.X, 255)
        self.assertEqual(self.CPU.negative, 1)
        self.assertEqual(self.CPU.zero, 0)
        self.assertEqual(self.CPU.cycles, 2)
    def testDEY(self):
        #check at 1
        self.CPU.reset()
        self.CPU.Y = 1
        self.CPU.memory[0] = 0x88
        self.CPU.step()
        self.assertEqual(self.CPU.Y, 0)
        self.assertEqual(self.CPU.negative, 0)
        self.assertEqual(self.CPU.zero, 1)
        self.assertEqual(self.CPU.cycles, 2)
        
        #check a negative number
        self.CPU.reset()
        self.CPU.Y = 0xFF
        self.CPU.memory[0] = 0x88
        self.CPU.step()
        self.assertEqual(self.CPU.Y, 0xFE)
        self.assertEqual(self.CPU.negative, 1)
        self.assertEqual(self.CPU.zero, 0)
        self.assertEqual(self.CPU.cycles, 2)
        
        #check wraparound
        self.CPU.reset()
        self.CPU.Y = 0
        self.CPU.memory[0] = 0x88
        self.CPU.step()
        self.assertEqual(self.CPU.Y, 255)
        self.assertEqual(self.CPU.negative, 1)
        self.assertEqual(self.CPU.zero, 0)
        self.assertEqual(self.CPU.cycles, 2)
        
        
class TestStatusRegisterOpcodes(TestCPUTemplate):
    #Status Register Operations
    def testCLC(self):

        self.CPU.reset()
        self.CPU.carry = 1
        
        self.CPU.memory[0] = 0x18
        self.CPU.step()
        self.assertEqual(0, self.CPU.carry)
        self.assertEqual(2, self.CPU.cycles)

    def testCLD(self):
        self.CPU.reset()
        self.CPU.decimal = 1
        
        self.CPU.memory[0] = 0xD8
        self.CPU.step()
        self.assertEqual(0, self.CPU.decimal)
        self.assertEqual(2, self.CPU.cycles)

    def testCLI(self):
        self.CPU.reset()
        self.CPU.int_disable = 1
        
        self.CPU.memory[0] = 0x58
        self.CPU.step()
        self.assertEqual(0, self.CPU.int_disable)
        self.assertEqual(2, self.CPU.cycles)
        
    def testCLV(self):
        self.CPU.reset()
        self.CPU.overflow = 1
        
        self.CPU.memory[0] = 0xB8
        self.CPU.step()
        self.assertEqual(0, self.CPU.overflow)
        self.assertEqual(2, self.CPU.cycles)
        
    def testSEC(self):
        self.CPU.reset()
        self.CPU.carry = 0
        
        self.CPU.memory[0] = 0x38
        self.CPU.step()
        self.assertEqual(1, self.CPU.carry)
        self.assertEqual(2, self.CPU.cycles)
        
    def testSED(self):
        self.CPU.reset()
        self.CPU.decimal = 0
        
        self.CPU.memory[0] = 0xF8
        self.CPU.step()
        self.assertEqual(1, self.CPU.decimal)
        self.assertEqual(2, self.CPU.cycles)
        
    def testSEI(self):
        self.CPU.reset()
        self.CPU.int_disable = 0
        
        self.CPU.memory[0] = 0x78
        self.CPU.step()
        self.assertEqual(1, self.CPU.int_disable)
        self.assertEqual(2, self.CPU.cycles)

class TestSpecialOpcodes(TestCPUTemplate):        
    #Special Operations
    def testNOP(self):
        self.CPU.reset()
        self.CPU.memory[0] = 0xEA
        self.CPU.step()
        #make sure it didn't change any registers
        self.assertEqual(0x20, self.CPU.PS)
        self.assertEqual(0,    self.CPU.X) 
        self.assertEqual(0,    self.CPU.Y)
        self.assertEqual(0,    self.CPU.A)
        self.assertEqual(0xFF, self.CPU.S)
        
        #make sure it actually did advance the cycles and PC.
        self.assertEqual(2, self.CPU.cycles)
        self.assertEqual(1, self.CPU.PC)
        
if __name__ == '__main__':
    #unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAddressingModes)
    unittest.TextTestRunner(verbosity=2).run(suite)
