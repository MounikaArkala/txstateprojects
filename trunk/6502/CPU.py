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
        #optable is of form Opcode: (function, function_parameters(usually addressing mode))
        self.optable = { \
        
        #Branches
        0xB0 : ("Branch Carry Set",      "BCS", self.BCS, None),
        0x90 : ("Branch Carry Clear",    "BCC", self.BCC, None),
        0xF0 : ("Branch Zero Set",       "BEQ", self.BEQ, None),
        0xD0 : ("Branch Zero Clear",     "BNE", self.BNE, None),
        0x30 : ("Branch Negative Set",   "BMI", self.BMI, None),
        0x10 : ("Branch Negative Clear", "BPL", self.BPL, None),
        0x70 : ("Branch Overflow Set",   "BVS", self.BVS, None),
        0x50 : ("Branch Overflow Clear", "BVC", self.BVC, None),
        
        
        
        #Register Transfer Ops
        0x9A : ("Transfer X to S",       "TXS", self.TXS, None),
        0xBA : ("Transfer S to X",       "TSX", self.TSX, None),
        0x8A : ("Transfer X to A",       "TXA", self.TXA, None),
        0xAA : ("Transfer A to X",       "TAX", self.TAX, None),
        0x98 : ("Transfer Y to A",       "TYA", self.TYA, None),
        0xA8 : ("Transfer A to Y",       "TAY", self.TAY, None),
        
        #Stack Ops
        0x48 : ("Push A",                "PHA", self.PHA, None),
        0x08 : ("Push Processor Status", "PHP", self.PHP, None),
        0x68 : ("Pull A",                "PLA", self.PLA, None),
        0x28 : ("Pull Processor Status", "PLP", self.PLP, None),
        
        #Status Register Ops
        0x18 : ("Clear Carry",        "CLC", self.CLC, None),
        0xD8 : ("Clear Decimal",      "CLD", self.CLD, None),
        0x58 : ("Clear Int. Disable", "CLI", self.CLI, None),
        0xB8 : ("Clear Overflow",     "CLV", self.CLV, None),
        0x38 : ("Set Carry",          "SEC", self.SEC, None),
        0xF8 : ("Set Decimal",        "SED", self.SED, None),
        0x78 : ("Set Int. Disable",   "SEI", self.SEI, None),
        
        
        #Arithmetic Operations
        0x69 : ("Add with Carry (Immediate)",  "ADC IMM", self.ADC, self.A_IMM),
        0x6D : ("Add with Carry (Absolute)",   "ADC ABS", self.ADC, self.A_ABS),
        0x65 : ("Add with Carry (Zero Page)",  "ADC ZPG", self.ADC, self.A_ZPG),
        0x7D : ("Add with Carry (Absolute X)", "ADC ABX", self.ADC, self.A_ABX),
        0x79 : ("Add with Carry (Absolute Y)", "ADC ABY", self.ADC, self.A_ABY),
        0x61 : ("Add with Carry (Indirect X)", "ADC IDX", self.ADC, self.A_IDX),
        
        
        #Increments / Decrements
        0xE8 : ("Increment X",        "INX", self.INX, None),
        0xC8 : ("Increment Y",        "INX", self.INY, None),
        0xCA : ("Decrement X",        "DEX", self.DEX, None),
        0x88 : ("Decrement Y",        "DEY", self.DEY, None),
        
        #Special Ops
        0xEA : ("No Operation",       "NOP", self.NOP, None),
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
        
    def A_ABX(self):
        self.cycles += 2
        self.PC += 2
        destaddr = (self.read(self.PC-1) << 8) + self.read(self.PC-2) + self.X
        if destaddr / 256 != self.PC / 256:
            # add an extra cycle for crossing page boundary.
            self.cycles += 1
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
        
        
    def clear_memory(self):
        self.memory = [0]*0x10000

    def step(self):
        opcode = self.read(self.PC)
        self.PC += 1
        try:
            op = self.optable[opcode]
            debug("executing a %s" % op[0])
            if (op[3]):
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
        need to be taken care of involvind that address."""
        self.memory[addr] = value

    def read(self, addr):
        return self.memory[addr]

        
        
        
    #|====================|
    #|===|   OPCODES  |===|
    #|====================|
    
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
    
    # ----------------------------
    # ---- Logical Operations ----
    # ----------------------------
    # Perform logical operations on the accumulator
    # and a value stored in memory.
    
    # Shifts - Shift the bits of either the accumulator or a memory location one bit to the left or right. 
    
    
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
    def makebin(self,val):
        table = {0x0: "0000",0x1:"0001",0x2:"0010",0x3:"0011",0x4:"0011",0x5: "0101",0x6:"0110",0x7:"0111",0x8:"1000",0x9:"1001",
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
        
        #TODO: should carry be added to this before checking if it's negative?
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
    
 
 
    #Load / Store Operations - Load a register from memory or stores the contents of a register to memory. 
    #Jumps / Calls - Break sequential execution sequence, resuming from a specified address. 
    
    
    #Branches - Break sequential execution sequence, resuming from a specified address, if a condition is met. The condition involves examining a specific bit in the status register.
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
