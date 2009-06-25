"""Unit test for CPU.py"""

import CPU
import unittest

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


class TestCPUFunctions(unittest.TestCase):

    def setUp(self):
        self.CPU = CPU.c6502()

    def testClearMemory(self):
        self.CPU.clear_memory()
        self.assertEqual(0, sum(self.CPU.memory))
    
    
    
        

class TestOpcodes(unittest.TestCase):
    def setUp(self):
        self.CPU = CPU.c6502()
    
    
    #OPCODE TESTS
    
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
    
    
    def loadMem(self, offset, vals):
        for i in range(len(vals)):
            self.CPU.memory[offset + i] = vals[i]
    
    
    
    
    
    
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
        
        
        
        
        
        
        
        
        
        
        
    #Logical Operations - Perform logical operations on the accumulator and a value stored in memory.
    
    # Shifts - Shift the bits of either the accumulator or a memory location one bit to the left or right. 
    
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
    
    #Arithmetic Operations - Perform arithmetic operations on registers and memory. 
    def testADC(self):
        pass
    
    def testSBC(self):
        pass
    
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

        
        
        
        
    #Functionality tests  
    def testPS(self):
        for i in range(0x100):
            self.CPU.PS = i #test setting self.CPU.PS
            self.assertEqual(i | 0x20, self.CPU.PS) #test getting self.CPU.PS as well.
        
    """
    def testsample(self):
        self.assertRaises(ValueError, random.sample, self.seq, 20)
        for element in random.sample(self.seq, 5):
            self.assert_(element in self.seq)"""

if __name__ == '__main__':
    unittest.main()
