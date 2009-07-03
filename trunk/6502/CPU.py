DEBUG = 0
def debug(astr):
    global DEBUG
    if DEBUG:
        print "\n%s\n" % astr


class Interrupt(object):

    def __init__(self, t="NMI"):
        self.type = t

        
        
            
def getLow(val, num_bits, size=16):
    return val & (2**num_bits - 1)
    # eg. for 16, 8 will yield (val & 0000000011111111)
    
def getHigh(val, num_bits, size=16):
    return val & ((2**size - 1) - (2**(size-num_bits) - 1))
    # eg. for 16, 8 will yield val & 1111111100000000


def unSign(val, size=8): #takes in a 2's complement number, returns a non-complemented form.
    if val >> (size-1):# need to take 2's complement
        temp = 2**size - 1
        val ^= temp #XOR to flip bits
        val += 1 # add 1
        val = 0 - val
        return val
        
    else: #just return val as-is
        return val
        

        
        
        
        
        
class c6502(object):

    def _getStatus(self):
        return (self.negative    << 7) + \
               (self.overflow    << 6) + \
               0x20                    + \
               (self.brk         << 4) + \
               (self.decimal     << 3) + \
               (self.int_disable << 2) + \
               (self.zero        << 1) + \
               self.carry
               
    def _setStatus(self, val):
        self.negative    = (val & 0x80) >> 7
        self.overflow    = (val & 0x40) >> 6
        self.brk         = (val & 0x10) >> 4
        self.decimal     = (val & 0x08) >> 3
        self.int_disable = (val & 0x04) >> 2
        self.zero        = (val & 0x02) >> 1
        self.carry       = (val & 0x01)
    
    
    PS = property(_getStatus, _setStatus) # processor status
    

    def __init__(self):
        #optable is of form Opcode: (longname, shortname, implementation, readmem, writemem)
        #if it doesn't require any read/write ability to memory, just place None's in those locations.
        self.optable = { \
        
        #Logical
        0x29 : ("AND (Immediate)",   "AND IMM", self.AND, self.A_IMM, None),
        0x25 : ("AND (Zero Page)",   "AND ZPG", self.AND, self.A_ZPG, None),
        0x35 : ("AND (Zero Page X)", "AND ZPX", self.AND, self.A_ZPX, None),
        0x2D : ("AND (Absolute)",    "AND ABS", self.AND, self.A_ABS, None),
        0x3D : ("AND (Absolute X)",  "AND ABX", self.AND, self.A_ABX, None),
        0x39 : ("AND (Absolute Y)",  "AND ABY", self.AND, self.A_ABY, None),
        0x21 : ("AND (Indirect X)",  "AND IDX", self.AND, self.A_IDX, None),
        0x31 : ("AND (Indirect Y)",  "AND IDY", self.AND, self.A_IDY, None),

        0x49 : ("Exclusive OR (Immediate)",   "EOR IMM", self.EOR, self.A_IMM, None),
        0x45 : ("Exclusive OR (Zero Page)",   "EOR ZPG", self.EOR, self.A_ZPG, None),
        0x55 : ("Exclusive OR (Zero Page X)", "EOR ZPX", self.EOR, self.A_ZPX, None),
        0x4D : ("Exclusive OR (Absolute)",    "EOR ABS", self.EOR, self.A_ABS, None),
        0x5D : ("Exclusive OR (Absolute X)",  "EOR ABX", self.EOR, self.A_ABX, None),
        0x59 : ("Exclusive OR (Absolute Y)",  "EOR ABY", self.EOR, self.A_ABY, None),
        0x41 : ("Exclusive OR (Indirect X)",  "EOR IDX", self.EOR, self.A_IDX, None),
        0x51 : ("Exclusive OR (Indirect Y)",  "EOR IDY", self.EOR, self.A_IDY, None),
        
        0xC9 : ("Compare to Accumulator (Immediate)",   "CMP IMM", self.CMP, self.A_IMM, None),
        0xC5 : ("Compare to Accumulator (Zero Page)",   "CMP ZPG", self.CMP, self.A_ZPG, None),
        0xD5 : ("Compare to Accumulator (Zero Page X)", "CMP ZPX", self.CMP, self.A_ZPX, None),
        0xCD : ("Compare to Accumulator (Absolute)",    "CMP ABS", self.CMP, self.A_ABS, None),
        0xDD : ("Compare to Accumulator (Absolute X)",  "CMP ABX", self.CMP, self.A_ABX, None),
        0xD9 : ("Compare to Accumulator (Absolute Y)",  "CMP ABY", self.CMP, self.A_ABY, None),
        0xC1 : ("Compare to Accumulator (Indirect X)",  "CMP IDX", self.CMP, self.A_IDX, None),
        0xD1 : ("Compare to Accumulator (Indirect Y)",  "CMP IDY", self.CMP, self.A_IDY, None),
        
        0xE0 : ("Compare to X (Immediate)",   "CPX IMM", self.CPX, self.A_IMM, None),
        0xE4 : ("Compare to X (Zero Page)",   "CPX ZPG", self.CPX, self.A_ZPG, None),
        0xEC : ("Compare to X (Absolute)",    "CPX ABS", self.CPX, self.A_ABS, None),
        
        0xC0 : ("Compare to Y (Immediate)",   "CPY IMM", self.CPY, self.A_IMM, None),
        0xC4 : ("Compare to Y (Zero Page)",   "CPY ZPG", self.CPY, self.A_ZPG, None),
        0xCC : ("Compare to Y (Absolute)",    "CPY ABS", self.CPY, self.A_ABS, None),
        
        
        
        #Shifts       
        0x0A : ("Arithmetic Shift Left (Accumulator)", "ASL IMM", self.ASL, self.A_ACC,      self.W_ACC),
        0x06 : ("Arithmetic Shift Left (Zero Page)",   "ASL ZPG", self.ASL, self.A_ZPG,      self.W_ZPG),
        0x16 : ("Arithmetic Shift Left (Zero Page X)", "ASL ZPX", self.ASL, self.A_ZPX,      self.W_ZPX),
        0x0E : ("Arithmetic Shift Left (Absolute)",    "ASL ABS", self.ASL, self.A_ABS,      self.W_ABS),
        0x1E : ("Arithmetic Shift Left (Absolute X)",  "ASL ABX", self.ASL, self.A_ABX_NOPB, self.W_ABX),
        
        #Branches
        0xB0 : ("Branch Carry Set",      "BCS", self.BCS, None, None),
        0x90 : ("Branch Carry Clear",    "BCC", self.BCC, None, None),
        0xF0 : ("Branch Zero Set",       "BEQ", self.BEQ, None, None),
        0xD0 : ("Branch Zero Clear",     "BNE", self.BNE, None, None),
        0x30 : ("Branch Negative Set",   "BMI", self.BMI, None, None),
        0x10 : ("Branch Negative Clear", "BPL", self.BPL, None, None),
        0x70 : ("Branch Overflow Set",   "BVS", self.BVS, None, None),
        0x50 : ("Branch Overflow Clear", "BVC", self.BVC, None, None),
        
        
        
        #Register Transfer Ops
        0x9A : ("Transfer X to S",       "TXS", self.TXS, None, None),
        0xBA : ("Transfer S to X",       "TSX", self.TSX, None, None),
        0x8A : ("Transfer X to A",       "TXA", self.TXA, None, None),
        0xAA : ("Transfer A to X",       "TAX", self.TAX, None, None),
        0x98 : ("Transfer Y to A",       "TYA", self.TYA, None, None),
        0xA8 : ("Transfer A to Y",       "TAY", self.TAY, None, None),
        
        #Stack Ops
        0x48 : ("Push A",                "PHA", self.PHA, None, None),
        0x08 : ("Push Processor Status", "PHP", self.PHP, None, None),
        0x68 : ("Pull A",                "PLA", self.PLA, None, None),
        0x28 : ("Pull Processor Status", "PLP", self.PLP, None, None),
        
        #Status Register Ops
        0x18 : ("Clear Carry",        "CLC", self.CLC, None, None),
        0xD8 : ("Clear Decimal",      "CLD", self.CLD, None, None),
        0x58 : ("Clear Int. Disable", "CLI", self.CLI, None, None),
        0xB8 : ("Clear Overflow",     "CLV", self.CLV, None, None),
        0x38 : ("Set Carry",          "SEC", self.SEC, None, None),
        0xF8 : ("Set Decimal",        "SED", self.SED, None, None),
        0x78 : ("Set Int. Disable",   "SEI", self.SEI, None, None),
        
        
        #Arithmetic Operations
        0x69 : ("Add with Carry (Immediate)",   "ADC IMM", self.ADC, self.A_IMM, None),
        0x65 : ("Add with Carry (Zero Page)",   "ADC ZPG", self.ADC, self.A_ZPG, None),
        0x75 : ("Add with Carry (Zero Page X)", "ADC IDX", self.ADC, self.A_ZPX, None),
        0x6D : ("Add with Carry (Absolute)",    "ADC ABS", self.ADC, self.A_ABS, None),
        0x7D : ("Add with Carry (Absolute X)",  "ADC ABX", self.ADC, self.A_ABX, None),
        0x79 : ("Add with Carry (Absolute Y)",  "ADC ABY", self.ADC, self.A_ABY, None),
        0x61 : ("Add with Carry (Indirect X)",  "ADC IDX", self.ADC, self.A_IDX, None),
        0x71 : ("Add with Carry (Indirect Y)",  "ADC IDY", self.ADC, self.A_IDY, None),
        
        
        #Increments / Decrements
        0xE8 : ("Increment X",        "INX", self.INX, None, None),
        0xC8 : ("Increment Y",        "INX", self.INY, None, None),
        0xCA : ("Decrement X",        "DEX", self.DEX, None, None),
        0x88 : ("Decrement Y",        "DEY", self.DEY, None, None),
        
        
        
        #Control
        #0x4c: ("Jump", "JMP ABS", self.JPA, 
        
        
        #Special Ops
        0xEA : ("No Operation",       "NOP", self.NOP, None, None),
        }
        
        self.reset()
        
        
        
        
    
    #All of the different addressing modes
    def A_IMM(self):
        self.PC += 1
        return self.read(self.PC-1)
        
    def A_ABS(self):
        self.cycles += 2
        self.PC += 2
        return self.read((self.read(self.PC-1) << 8) + self.read(self.PC-2))
        
    def A_ZPG(self):
        self.cycles += 1
        self.PC += 1
        return self.read(self.read(self.PC-1))
        
    def A_ZPX(self):
        self.cycles += 2
        self.PC += 1
        return self.read((self.read(self.PC-1) + self.X) % 256)
    
    def A_ABX(self):
        self.cycles += 2
        self.PC += 2
        destaddr = (self.read(self.PC-1) << 8) + self.read(self.PC-2) + self.X
        if destaddr / 256 != self.PC / 256:
            # add an extra cycle for crossing page boundary.
            self.cycles += 1
        return self.read(destaddr)
        
    def A_ABX_NOPB(self):
        #doesn't check for page boundary, always costs 3
        self.cycles += 3
        self.PC += 2
        destaddr = (self.read(self.PC-1) << 8) + self.read(self.PC-2) + self.X
        return self.read(destaddr)
        
    def A_ABY(self):
        self.cycles += 2
        self.PC += 2
        destaddr = (self.read(self.PC-1) << 8) + self.read(self.PC-2) + self.Y
        if destaddr / 256 != self.PC / 256:
            # add an extra cycle for crossing page boundary.
            self.cycles += 1
        return self.read(destaddr)
        
    def A_IDX(self):
        self.cycles += 4
        #Wrap around to keep in ZP
        zpaddr = (self.read(self.PC) + self.X) % 256
        self.PC += 1
        destaddr = (self.read(zpaddr+1) << 8) + self.read(zpaddr)
        return self.read(destaddr)
        
    def A_IDY(self):
        self.cycles += 3
        
        #Wrap around to keep in ZP
        zpaddr = self.read(self.PC)
        self.PC += 1
        destaddr = (self.read(zpaddr+1) << 8) + self.read(zpaddr) + self.Y
        if destaddr / 256 != self.PC / 256:
            # add an extra cycle for crossing page boundary.
            self.cycles += 1
        return self.read(destaddr)
        
    def A_ACC(self):
        return self.A
    
    def W_ACC(self, val):
        self.A = val
    
    def W_ZPG(self, val):
        self.write(self.read(self.PC - 1), val)
        self.cycles += 2
    
    def W_ZPX(self, val):
        self.write((self.read(self.PC - 1) + self.X) % 256, val)
        self.cycles += 2
    
    def W_ABS(self, val):
        self.write(((self.read(self.PC - 1) << 8) + self.read(self.PC - 2)), val)
        self.cycles += 2
    
    def W_ABX(self, val):
        self.write(((self.read(self.PC - 1) << 8) + self.read(self.PC - 2) + self.X), val)
        self.cycles += 2
        
        
        
        
        
    def clear_memory(self):
        self.memory = [0]*0x10000

    def step(self):
        print "stepping..."
        opcode = self.read(self.PC)
        print "opcode: ", hex(opcode)
        self.PC += 1
        try:
            op = self.optable[opcode]
            debug("executing a %s" % op[0])
            if (op[3]):
                if (op[4]):
                    op[2](op[3](), op[4])
                else:
                    op[2](op[3]())
            else:
                op[2]()
                
        except KeyError:
            debug("Invalid OPCODE (%s)" % opcode)
            self.UnsupportedOpcode()
            #TODO: raise UnsupportedOpcode exception here
            
            
    def reset(self):
        self.clear_memory() # init memory
        self.X      = 0     # X index register
        self.Y      = 0     # Y index register
        self.A      = 0     # Accumulator
        self.S      = 0xFF  # Stack Pointer
        self.PC     = 0     # Program Counter
        self.PS     = 0     # Processor Status
        self.cycles = 0     # Cycle Count

    def write(self, addr, value):
        """ writes a value to a memory location.
        also handles any interrupts / mirroring that may 
        need to be taken care of involving that address."""
        self.memory[addr] = value

    def read(self, addr):
        return self.memory[addr]

        
        
        
    #|========================================================|
    #|=====================|   OPCODES  |=====================|
    #|========================================================|
    
    #Memory Operations
    
    # ----------------------------
    # ---- Logical Operations ----
    # ----------------------------
    # Perform logical operations on the accumulator
    # and a value stored in memory.
    
    def AND(self, val):
        self.A &= val
        self.cycles += 2
    
    def ROL(self, val):
        #rotate left
        pass
    
    def ROR(self, val):
        #rotate right
        pass
    def BIT(self, val):
        #Test bit
        pass
    
    def CMP(self, val):
        #compare val to accumulator
        #interpret val as a 2's complement number
        val = unSign(val)
        if self.A > val:
            self.negative = 0
            self.zero = 0
            self.carry = 1
        elif self.A < val:
            self.negative = 1
            self.zero = 0
            self.carry = 0
        else:
            self.negative = 0
            self.zero = 1
            self.carry = 1
        self.cycles += 2       
        
    def CPX(self, val):
        val = unSign(val)
        if self.X > val:
            self.negative = 0
            self.zero = 0
            self.carry = 1
        elif self.X < val:
            self.negative = 1
            self.zero = 0
            self.carry = 0
        else:
            self.negative = 0
            self.zero = 1
            self.carry = 1
        self.cycles += 2
        
    def CPY(self, val):
        val = unSign(val)
        if self.Y > val:
            self.negative = 0
            self.zero = 0
            self.carry = 1
        elif self.Y < val:
            self.negative = 1
            self.zero = 0
            self.carry = 0
        else:
            self.negative = 0
            self.zero = 1
            self.carry = 1
        self.cycles += 2
    
    def EOR(self, val):
        #exclusive or
        self.A ^= val
        self.negative = self.A >> 7
        if (self.A == 0):
            self.zero = 1
        else:
            self.zero = 0
        self.cycles += 2
    #Load / Store Operations - Load a register from memory or stores the contents of a register to memory. 
    
    #Jumps / Calls - Break sequential execution sequence, resuming from a specified address. 
    def JMP(self, val):
        pass
    
    # Shifts - Shift the bits of either the accumulator or a memory location one bit to the left or right. 
    def ASL(self, val, writer):
        self.carry = val >> 7
        val &= 0x7F
        val = val << 1
        self.zero = (val == 0)
        self.negative = val >> 7
        writer(val)
        self.cycles += 2
    
    # --------------------------------------
    # ---- Register Transfer Operations ----
    # --------------------------------------
    # Copy contents of X or Y register to Accumulator
    # or copy contents of Accumulator to X or Y register. 
    def TXS(self):
        self.S = self.X
        self.cycles += 2
        
    def TSX(self):
        self.X = self.S
        self.negative = self.X >> 7
        if self.X == 0:
            self.zero = 1
        else:
            self.zero = 0
        self.cycles += 2
        
    def TXA(self):
        self.A = self.X
        self.negative = self.A >> 7
        if self.A == 0:
            self.zero = 1
        else:
            self.zero = 0
        self.cycles += 2
        
    def TAX(self):
        self.X = self.A
        self.negative = self.A >> 7
        if self.A == 0:
            self.zero = 1
        else:
            self.zero = 0
        self.cycles += 2
        
    def TYA(self):
        self.A = self.Y
        self.negative = self.A >> 7
        if self.A == 0:
            self.zero = 1
        else:
            self.zero = 0
        self.cycles += 2
        
    def TAY(self):
        self.Y = self.A
        self.negative = self.A >> 7
        if self.A == 0:
            self.zero = 1
        else:
            self.zero = 0
        self.cycles += 2
    
    
    #Stack Operations - Push or pull the stack or manipulate stack pointer using X register. 
    def PHA(self):
        self.write(self.S + 0x100, self.A)
        self.S -= 1
        if self.S < 0:
            self.S = 0 #TODO: raise exception?
        self.cycles += 3
        
    def PHP(self):
    
        self.write(self.S + 0x100, self.PS)
        self.S -= 1
        if self.S < 0:
            self.S = 0 #TODO: raise exception?
        self.cycles += 3
        
    def PLA(self):
        self.S += 1
        if self.S > 0xFF:
            self.S = 0xFF #TODO: raise exception?
        self.A = self.read(self.S + 0x100)
        self.negative = self.A >> 7 # bit 7 is negative bit
        if self.A == 0:
            self.zero = 1
        else:
            self.zero = 0
        self.cycles += 4
        
    def PLP(self):
        self.S += 1
        if self.S > 0xFF:
            self.S = 0xFF #TODO: raise exception?
        self.PS = self.read(self.S + 0x100)
        self.cycles += 4
    
    
    #Arithmetic Operations - Perform arithmetic operations on registers and memory.
    #TODO: relocate this function to a more appropriate class.
    def makebin(self,val):
        table = {0x0: "0000",0x1:"0001",0x2:"0010",0x3:"0011",0x4:"0100",0x5: "0101",0x6:"0110",0x7:"0111",0x8:"1000",0x9:"1001",
                 0xA: "1010",0xB:"1011",0xC:"1100",0xD:"1101",0xE:"1110",0xF:"1111"}
                 
        return table[val >> 4] + table[val & 0xF]
    
    
    def ADC(self, inc):
        inc %= 256
        debug("A is:      " + self.makebin(self.A))
        debug("inc is:    " + self.makebin(inc))
        debug("Status is: " + self.makebin(self.PS))
        self.negative = self.A >> 7
        
        self.A += inc + self.carry
            
        if self.A >= 2**8:
            self.A -= 2**8
            self.carry = 1
        else:
            self.carry = 0
        
        #this shouldn't ever happen!!
        if self.A < 0:
            self.A = (2**8) + inc
            debug("value went below 0 on an unsigned add!")
            
        if self.A == 0:
            self.zero = 1
        
        inc_neg = inc >> 7
        #if both were negative (1 , 1) and result was positive (0), then overflow = 1
        #if both were positive (0 , 0) and result was negative (1), then overflow = 1
        #if one was positive and one was negative, then there can't be overflow!!
        
        if (inc_neg ^ self.negative) == 0:
            if self.negative and (self.A >> 7 == 0):
                self.overflow = 1
            elif (not self.negative) and (self.A >> 7):
                self.overflow = 1
            else:
                #I don't get how this can happen but it does.
                self.overflow = 0
        else:
            self.overflow = 0
        
        self.negative = self.A >> 7 # set negative to the new negative value.
        debug("A is now: " + self.makebin(self.A))
        debug("Status is now: " + self.makebin(self.PS))
        self.cycles += 2
    
 
 
    
    
    #Branches - Break sequential execution sequence, resuming from a specified address,
    #if a condition is met. The condition involves examining a specific bit in the status register.
    def _BRANCH(self, val, comp):
        """ Compare val with comp, and if they're equal, do a branch."""
        displacement = self.read(self.PC)
        self.PC += 1
        self.cycles += 2
        if val == comp:
            self.cycles += 1
            dest = self.PC + unSign(displacement)
            if (self.PC / 256) != (dest / 256):
                self.cycles += 1 #page boundary.
            self.PC = dest
        
    def BCC(self):
        self._BRANCH(self.carry, 0)
        
    def BCS(self):
        self._BRANCH(self.carry, 1)
        
    def BEQ(self):
        self._BRANCH(self.zero, 1)
        
    def BNE(self):
        self._BRANCH(self.zero, 0)
            
    def BMI(self):
        self._BRANCH(self.negative, 1)
        
    def BPL(self):
        self._BRANCH(self.negative, 0)
        
    def BVC(self):
        self._BRANCH(self.overflow, 0)
        
    def BVS(self):
        self._BRANCH(self.overflow, 1)
        
 
    #Increments / Decrements - Increment or decrement the X or Y registers or a value stored in memory. 
    def INX(self):
        self.X += 1
        if self.X >= 256:
            self.X = 0
        self.negative = self.X >> 7
        if self.X == 0:
            self.zero = 1
        else:
            self.zero = 0
        self.cycles += 2
        
    def DEX(self):
        self.X -= 1
        if self.X < 0:
            self.X = 255
        self.negative = self.X >> 7
        if self.X == 0:
            self.zero = 1
        else:
            self.zero = 0
        self.cycles += 2
        
    def INY(self):
        self.Y += 1
        if self.Y >= 256:
            self.Y = 0
        self.negative = self.Y >> 7
        if self.Y == 0:
            self.zero = 1
        else:
            self.zero = 0
        self.cycles += 2
        
    def DEY(self):
        self.Y -= 1
        if self.Y < 0:
            self.Y = 255
        self.negative = self.Y >> 7
        if self.Y == 0:
            self.zero = 1
        else:
            self.zero = 0
        self.cycles += 2
         
    def INC(self, val):
        #increment memory
        pass
    
    def DEC(self, val):
        #decrement memory
        pass
    
    #Status Register Operations - Set or clear a flag in the status register. 
    def CLC(self):
        self.carry = 0
        self.cycles += 2

    def CLD(self):
        self.decimal = 0
        self.cycles += 2

    def CLI(self):
        self.int_disable = 0
        self.cycles += 2
        
    def CLV(self):
        self.overflow = 0
        self.cycles += 2

    def SEC(self):
        self.carry = 1
        self.cycles += 2
        
    def SED(self):
        self.decimal = 1
        self.cycles += 2
        
    def SEI(self):
        self.int_disable = 1
        self.cycles += 2
        
    #Special Operations
    
    def BRK(self):
        pass
        
    def NOP(self):
        self.cycles += 2
        
    def UnsupportedOpcode(self):
        pass #TODO: raise UnsupportedOpcode exception here
        
 #System Functions - Perform rarely used functions. 
 
if __name__ == "__Main__":

    x = c6502()    
    x.carry = 1
    print x.PS
    
"""
Counter=InterruptPeriod;
PC=InitialPC;

for(;;)
{
  OpCode=Memory[PC++];
  Counter-=Cycles[OpCode];

  switch(OpCode)
  {
    case OpCode1:
    case OpCode2:
    ...
  }

  if(Counter<=0)
  {
    /* Check for interrupts and do other */
    /* cyclic tasks here                 */
    ...
    Counter+=InterruptPeriod;
    if(ExitRequired) break;
  }
}


Cyclic tasks are things which should periodically occur in an emulated machine, such as:

    * Screen refresh
    * VBlank and HBlank interrupts
    * Updating timers
    * Updating sound parameters
    * Updating keyboard/joysticks state
    * etc. 

In order to emulate such tasks, you should tie them to appropriate number of CPU cycles. For example, if CPU is supposed to run at 2.5MHz and the display uses 50Hz refresh frequency (standard for PAL video), the VBlank interrupt will have to occur every

       2500000/50 = 50000 CPU cycles

Now, if we assume that the entire screen (including VBlank) is 256 scanlines tall and 212 of them are actually shown at the display (i.e. other 44 fall into VBlank), we get that your emulation must refresh a scanline each

       50000/256 ~= 195 CPU cyles

After that, you should generate a VBlank interrupt and then do nothing until we are done with VBlank, i.e. for

       (256-212)*50000/256 = 44*50000/256 ~= 8594 CPU cycles

Carefully calculate numbers of CPU cycles needed for each task, then use their biggest common divisor for InterruptPeriod and tie all other tasks to it (they should not necessarily execute on every expiration of the Counter). 
"""
