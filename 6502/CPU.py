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
        
def Sign(val, size=8):#returns 2's complement form.
    
    if val >= 0:
        return val
    val = abs(val)
    temp = 2**size - 1
    val ^= temp #XOR to flip bits
    val += 1 # add 1
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
        
        0x09 : ("OR (Immediate)",   "ORA IMM", self.ORA, self.A_IMM, None),
        0x05 : ("OR (Zero Page)",   "ORA ZPG", self.ORA, self.A_ZPG, None),
        0x15 : ("OR (Zero Page X)", "ORA ZPX", self.ORA, self.A_ZPX, None),
        0x0D : ("OR (Absolute)",    "ORA ABS", self.ORA, self.A_ABS, None),
        0x1D : ("OR (Absolute X)",  "ORA ABX", self.ORA, self.A_ABX, None),
        0x19 : ("OR (Absolute Y)",  "ORA ABY", self.ORA, self.A_ABY, None),
        0x01 : ("OR (Indirect X)",  "ORA IDX", self.ORA, self.A_IDX, None),
        0x11 : ("OR (Indirect Y)",  "ORA IDY", self.ORA, self.A_IDY, None),

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
        
        0x24 : ("Bit Test", "BIT ZPG", self.BIT, self.A_ZPG, None),
        0x2C : ("Bit Test", "BIT ZBS", self.BIT, self.A_ABS, None),
        
        
        #Memory
        0xA9 : ("Load Accumulator (Immediate)",   "LDA IMM", self.LDA, self.A_IMM, None),
        0xA5 : ("Load Accumulator (Zero Page)",   "LDA ZPG", self.LDA, self.A_ZPG, None),
        0xB5 : ("Load Accumulator (Zero Page X)", "LDA ZPX", self.LDA, self.A_ZPX, None),
        0xAD : ("Load Accumulator (Absolute)",    "LDA ABS", self.LDA, self.A_ABS, None),
        0xBD : ("Load Accumulator (Absolute X)",  "LDA ABX", self.LDA, self.A_ABX, None),
        0xB9 : ("Load Accumulator (Absolute Y)",  "LDA ABY", self.LDA, self.A_ABY, None),
        0xA1 : ("Load Accumulator (Indirect X)",  "LDA IDX", self.LDA, self.A_IDX, None),
        0xB1 : ("Load Accumulator (Indirect Y)",  "LDA IDY", self.LDA, self.A_IDY, None),
        
        0xA2 : ("Load X (Immediate)",    "LDX IMM", self.LDX, self.A_IMM, None),
        0xA6 : ("Load X (Zero Page)",    "LDX ZPG", self.LDX, self.A_ZPG, None),
        0xB6 : ("Load X (Zero Page Y)",  "LDX IDY", self.LDX, self.A_ZPY, None), #NOTE ZPY not ZPX!!!
        0xAE : ("Load X (Absolute)",     "LDX ABS", self.LDX, self.A_ABS, None),
        0xBE : ("Load X (Absolute Y)",   "LDX ABY", self.LDX, self.A_ABY, None),
        
        0xA0 : ("Load Y (Immediate)",   "LDY IMM", self.LDY, self.A_IMM, None),
        0xA4 : ("Load Y (Zero Page)",   "LDY ZPG", self.LDY, self.A_ZPG, None),
        0xB4 : ("Load Y (Zero Page X)", "LDY ZPX", self.LDY, self.A_ZPX, None),
        0xAC : ("Load Y (Absolute)",    "LDY ABS", self.LDY, self.A_ABS, None),
        0xBC : ("Load Y (Absolute X)",  "LDY ABX", self.LDY, self.A_ABX, None),
               
               
        0x85 : ("Store Accumulator (Zero Page)",   "STA ZPG", self.STA, lambda: self.F_ADD(1,1), self.W_ZPG),
        0x95 : ("Store Accumulator (Zero Page X)", "STA ZPX", self.STA, lambda: self.F_ADD(2,1), self.W_ZPX),
        0x8D : ("Store Accumulator (Absolute)",    "STA ABS", self.STA, lambda: self.F_ADD(2,2), self.W_ABS),
        0x9D : ("Store Accumulator (Absolute X)",  "STA ABX", self.STA, lambda: self.F_ADD(3,2), self.W_ABX),
        0x99 : ("Store Accumulator (Absolute Y)",  "STA ABY", self.STA, lambda: self.F_ADD(3,2), self.W_ABY),
        0x81 : ("Store Accumulator (Indirect X)",  "STA IDX", self.STA, lambda: self.F_ADD(4,1), self.W_IDX),
        0x91 : ("Store Accumulator (Indirect Y)",  "STA IDY", self.STA, lambda: self.F_ADD(4,1), self.W_IDY),
        
        0x86 : ("Store X (Zero Page)",   "STX ZPG", self.STX, lambda: self.F_ADD(1,1), self.W_ZPG),
        0x96 : ("Store X (Zero Page Y)", "STX ZPY", self.STX, lambda: self.F_ADD(2,1), self.W_ZPY), #NOTE ZPY not ZPX!!!
        0x8E : ("Store X (Absolute)",    "STX ABS", self.STX, lambda: self.F_ADD(2,2), self.W_ABS),
        
        0x84 : ("Store Y (Zero Page)",   "STY ZPG", self.STY, lambda: self.F_ADD(1,1), self.W_ZPG),
        0x94 : ("Store Y (Zero Page X)", "STY ZPX", self.STY, lambda: self.F_ADD(2,1), self.W_ZPX),
        0x8C : ("Store Y (Absolute)",    "STY ABS", self.STY, lambda: self.F_ADD(2,2), self.W_ABS),
        
        
        
        
        
        #Shifts       
        0x0A : ("Arithmetic Shift Left (Accumulator)", "ASL IMM", self.ASL, self.A_ACC,      self.W_ACC),
        0x06 : ("Arithmetic Shift Left (Zero Page)",   "ASL ZPG", self.ASL, self.A_ZPG,      self.W_ZPG),
        0x16 : ("Arithmetic Shift Left (Zero Page X)", "ASL ZPX", self.ASL, self.A_ZPX,      self.W_ZPX),
        0x0E : ("Arithmetic Shift Left (Absolute)",    "ASL ABS", self.ASL, self.A_ABS,      self.W_ABS),
        0x1E : ("Arithmetic Shift Left (Absolute X)",  "ASL ABX", self.ASL, self.A_ABX_NOPB, self.W_ABX),
        
        0x4A : ("Logical Shift Right (Accumulator)", "LSR IMM", self.LSR, self.A_ACC,      self.W_ACC),
        0x46 : ("Logical Shift Right (Zero Page)",   "LSR ZPG", self.LSR, self.A_ZPG,      self.W_ZPG),
        0x56 : ("Logical Shift Right (Zero Page X)", "LSR ZPX", self.LSR, self.A_ZPX,      self.W_ZPX),
        0x4E : ("Logical Shift Right (Absolute)",    "LSR ABS", self.LSR, self.A_ABS,      self.W_ABS),
        0x5E : ("Logical Shift Right (Absolute X)",  "LSR ABX", self.LSR, self.A_ABX_NOPB, self.W_ABX),
        
        0x2A : ("Rotate Left (Accumulator)", "ROL IMM", self.ROL, self.A_ACC,      self.W_ACC),
        0x26 : ("Rotate Left (Zero Page)",   "ROL ZPG", self.ROL, self.A_ZPG,      self.W_ZPG),
        0x36 : ("Rotate Left (Zero Page X)", "ROL ZPX", self.ROL, self.A_ZPX,      self.W_ZPX),
        0x2E : ("Rotate Left (Absolute)",    "ROL ABS", self.ROL, self.A_ABS,      self.W_ABS),
        0x3E : ("Rotate Left (Absolute X)",  "ROL ABX", self.ROL, self.A_ABX_NOPB, self.W_ABX),
        
        0x6A : ("Rotate Right (Accumulator)", "ROR IMM", self.ROR, self.A_ACC,      self.W_ACC),
        0x66 : ("Rotate Right (Zero Page)",   "ROR ZPG", self.ROR, self.A_ZPG,      self.W_ZPG),
        0x76 : ("Rotate Right (Zero Page X)", "ROR ZPX", self.ROR, self.A_ZPX,      self.W_ZPX),
        0x6E : ("Rotate Right (Absolute)",    "ROR ABS", self.ROR, self.A_ABS,      self.W_ABS),
        0x7E : ("Rotate Right (Absolute X)",  "ROR ABX", self.ROR, self.A_ABX_NOPB, self.W_ABX),
        
        
        
        
        #Branches
        0xB0 : ("Branch Carry Set",      "BCS", self.BCS, None, None),
        0x90 : ("Branch Carry Clear",    "BCC", self.BCC, None, None),
        0xF0 : ("Branch Zero Set",       "BEQ", self.BEQ, None, None),
        0xD0 : ("Branch Zero Clear",     "BNE", self.BNE, None, None),
        0x30 : ("Branch Negative Set",   "BMI", self.BMI, None, None),
        0x10 : ("Branch Negative Clear", "BPL", self.BPL, None, None),
        0x70 : ("Branch Overflow Set",   "BVS", self.BVS, None, None),
        0x50 : ("Branch Overflow Clear", "BVC", self.BVC, None, None),
        
        
        #Register Transfer
        0x9A : ("Transfer X to S",       "TXS", self.TXS, None, None),
        0xBA : ("Transfer S to X",       "TSX", self.TSX, None, None),
        0x8A : ("Transfer X to A",       "TXA", self.TXA, None, None),
        0xAA : ("Transfer A to X",       "TAX", self.TAX, None, None),
        0x98 : ("Transfer Y to A",       "TYA", self.TYA, None, None),
        0xA8 : ("Transfer A to Y",       "TAY", self.TAY, None, None),
        
        
        #Stack
        0x48 : ("Push A",                "PHA", self.PHA, None, None),
        0x08 : ("Push Processor Status", "PHP", self.PHP, None, None),
        0x68 : ("Pull A",                "PLA", self.PLA, None, None),
        0x28 : ("Pull Processor Status", "PLP", self.PLP, None, None),
        
        
        #Status Register
        0x18 : ("Clear Carry",        "CLC", self.CLC, None, None),
        0xD8 : ("Clear Decimal",      "CLD", self.CLD, None, None),
        0x58 : ("Clear Int. Disable", "CLI", self.CLI, None, None),
        0xB8 : ("Clear Overflow",     "CLV", self.CLV, None, None),
        0x38 : ("Set Carry",          "SEC", self.SEC, None, None),
        0xF8 : ("Set Decimal",        "SED", self.SED, None, None),
        0x78 : ("Set Int. Disable",   "SEI", self.SEI, None, None),
        
        
        #Arithmetic
        0x69 : ("Add with Carry (Immediate)",   "ADC IMM", self.ADC, self.A_IMM, None),
        0x65 : ("Add with Carry (Zero Page)",   "ADC ZPG", self.ADC, self.A_ZPG, None),
        0x75 : ("Add with Carry (Zero Page X)", "ADC IDX", self.ADC, self.A_ZPX, None),
        0x6D : ("Add with Carry (Absolute)",    "ADC ABS", self.ADC, self.A_ABS, None),
        0x7D : ("Add with Carry (Absolute X)",  "ADC ABX", self.ADC, self.A_ABX, None),
        0x79 : ("Add with Carry (Absolute Y)",  "ADC ABY", self.ADC, self.A_ABY, None),
        0x61 : ("Add with Carry (Indirect X)",  "ADC IDX", self.ADC, self.A_IDX, None),
        0x71 : ("Add with Carry (Indirect Y)",  "ADC IDY", self.ADC, self.A_IDY, None),
        
        0xE9 : ("Subtract with Carry (Immediate)",   "SBC IMM", self.SBC, self.A_IMM, None),
        0xE5 : ("Subtract with Carry (Zero Page)",   "SBC ZPG", self.SBC, self.A_ZPG, None),
        0xF5 : ("Subtract with Carry (Zero Page X)", "SBC ZPX", self.SBC, self.A_ZPX, None),
        0xED : ("Subtract with Carry (Absolute)",    "SBC ABS", self.SBC, self.A_ABS, None),
        0xFD : ("Subtract with Carry (Absolute X)",  "SBC ABX", self.SBC, self.A_ABX, None),
        0xF9 : ("Subtract with Carry (Absolute Y)",  "SBC ABY", self.SBC, self.A_ABY, None),
        0xE1 : ("Subtract with Carry (Indirect X)",  "SBC IDX", self.SBC, self.A_IDX, None),
        0xF1 : ("Subtract with Carry (Indirect Y)",  "SBC IDY", self.SBC, self.A_IDY, None),
        
        
        #Increments / Decrements
        0xE8 : ("Increment X",        "INX", self.INX, None, None),
        0xC8 : ("Increment Y",        "INX", self.INY, None, None),
        0xCA : ("Decrement X",        "DEX", self.DEX, None, None),
        0x88 : ("Decrement Y",        "DEY", self.DEY, None, None),
        
        0xC6 : ("Decrement (Zero Page)",   "DEC ZPG", self.DEC, self.A_ZPG,      self.W_ZPG),
        0xD6 : ("Decrement (Zero Page X)", "DEC ZPX", self.DEC, self.A_ZPX,      self.W_ZPX),
        0xCE : ("Decrement (Absolute)",    "DEC ABS", self.DEC, self.A_ABS,      self.W_ABS),
        0xDE : ("Decrement (Absolute X)",  "DEC ABX", self.DEC, self.A_ABX_NOPB, self.W_ABX),
        
        0xE6 : ("Increment (Zero Page)",   "INC ZPG", self.INC, self.A_ZPG,      self.W_ZPG),
        0xF6 : ("Increment (Zero Page X)", "INC ZPX", self.INC, self.A_ZPX,      self.W_ZPX),
        0xEE : ("Increment (Absolute)",    "INC ABS", self.INC, self.A_ABS,      self.W_ABS),
        0xFE : ("Increment (Absolute X)",  "INC ABX", self.INC, self.A_ABX_NOPB, self.W_ABX),
        
        
        #Special
        0xEA : ("No Operation",           "NOP",     self.NOP, None, None),
        0x00 : ("Break",                  "BRK",     self.BRK, None, None),
        0x4C : ("Jump Absolute",          "JMP ABS", self.JPA, None, None),
        0x6C : ("Jump Indirect",          "JMP IND", self.JPI, None, None),
        0x2D : ("Jump to Subroutine",     "JSR",     self.JSR, None, None),
        0x40 : ("Return from Interrupt",  "RTI",     self.RTI, None, None),
        0x60 : ("Return from Subroutine", "RTS",     self.RTS, None, None)
        
        
        }
        
        self.reset()
        
        
        
    #Adds cycles and advances PC, no other side effects.
    def F_ADD(self, cycles, bytes):
        self.cycles += cycles
        self.PC += bytes
        
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
        
    def A_ZPY(self):
        self.cycles += 2
        self.PC += 1
        return self.read((self.read(self.PC-1) + self.Y) % 256)    
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
    
    def W_ZPY(self, val):
        self.write((self.read(self.PC - 1) + self.Y) % 256, val)
        self.cycles += 2
    
    def W_ABS(self, val):
        self.write(((self.read(self.PC - 1) << 8) + self.read(self.PC - 2)), val)
        self.cycles += 2
    
    def W_ABX(self, val):
        self.write(((self.read(self.PC - 1) << 8) + self.read(self.PC - 2) + self.X), val)
        self.cycles += 2
        
    def W_ABY(self, val):
        self.write(((self.read(self.PC - 1) << 8) + self.read(self.PC - 2) + self.Y), val)
        self.cycles += 2
    
    def W_IDX(self, val):
        self.cycles += 2
        #Wrap around to keep in ZP
        zpaddr = (self.read(self.PC - 1) + self.X) % 256
        destaddr = (self.read(zpaddr+1) << 8) + self.read(zpaddr)
        self.write(destaddr, val)
        
    def W_IDY(self, val):
        self.cycles += 2
        #Wrap around to keep in ZP
        zpaddr = self.read(self.PC - 1)
        destaddr = (self.read(zpaddr+1) << 8) + self.read(zpaddr) + self.Y
        self.write(destaddr, val)
        
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
    
    
    # ---------------------------
    # ---- Memory Operations ----
    # ---------------------------
    
    def LDA(self, val):
        self.A = val
        self.negative = val >> 7
        if val == 0:
            self.zero = 1
        else:
            self.zero = 0
        self.cycles += 2
    
    def LDX(self, val):
        self.X = val
        self.negative = val >> 7
        if val == 0:
            self.zero = 1
        else:
            self.zero = 0
        self.cycles += 2
    
    def LDY(self, val):
        self.Y = val
        self.negative = val >> 7
        if val == 0:
            self.zero = 1
        else:
            self.zero = 0
        self.cycles += 2
    
    def STA(self, val, writer):
        writer(self.A)
        
    def STX(self, val, writer):
        writer(self.X)
        
    def STY(self, val, writer):
        writer(self.Y)
    
    # ----------------------------
    # ---- Logical Operations ----
    # ----------------------------
    # Perform logical operations on the accumulator
    # and a value stored in memory.
    
    def AND(self, val):
        self.A &= val
        self.negative = self.A >> 7
        if self.A == 0:
            self.zero = 1
        else:
            self.zero = 0
        self.cycles += 2
        
    def ORA(self, val):
        self.A |= val
        self.negative = self.A >> 7
        if self.A == 0:
            self.zero = 1
        else:
            self.zero = 0
        self.cycles += 2
        
    def BIT(self, val):
        #Test bit
        if self.A ^ val:
            self.zero = 0
        else:
            self.zero = 1
        self.negative = val >> 7
        self.overflow = (val & 0x40) >> 6
        self.cycles += 2
        
        
    
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
    
    # Shifts - Shift/rotate the bits of either the accumulator or a memory location one bit to the left or right. 
    def ASL(self, val, writer):
        self.carry = val >> 7
        val &= 0x7F
        val = val << 1
        if val == 0:
            self.zero = 1
        else:
            self.zero = 0
        self.negative = val >> 7
        writer(val)
        self.cycles += 2
        
    def LSR(self, val, writer):
        self.carry = val & 0x01
        val = val >> 1
        if val == 0:
            self.zero = 1
        else:
            self.zero = 0
        writer(val)
        self.cycles += 2
    
    def ROL(self, val, writer):
        #rotate left
        val = val << 1
        val += self.carry
        self.carry = val >> 8
        val &= 0xFF
        self.negative = val >> 7
        if val == 0:
            self.zero = 1
        else:
            self.zero = 0
        writer(val)
        self.cycles += 2
    
    def ROR(self, val, writer):
        #rotate right
        val += self.carry << 8
        self.carry = val & 0x01
        val = val >> 1
        self.negative = val >> 7
        if val == 0:
            self.zero = 1
        else:
            self.zero = 0
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
        #TODO: implement ADC with decimal support
        #inc %= 256
        #debug("A is:      " + self.makebin(self.A))
        #debug("inc is:    " + self.makebin(inc))
        #debug("Status is: " + self.makebin(self.PS))
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
            #debug("value went below 0 on an unsigned add!")
            
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
        #debug("A is now: " + self.makebin(self.A))
        #debug("Status is now: " + self.makebin(self.PS))
        self.cycles += 2
    
    
    def SBC(self, inc):
        #TODO: implement SBC with Decimal support.
        
        #inc %= 256
        #debug("A is:      " + self.makebin(self.A))
        #debug("inc is:    " + self.makebin(inc))
        #debug("Status is: " + self.makebin(self.PS))
        
        #SBC works the same as ADC but add carry and then negate the value of
        #inc before adding.
        if inc >> 7:#inc is negative
            inc = unSign(inc) + self.carry #TODO: HACK: this is probably wrong.
        else:
            inc = inc + (1 - self.carry)
        #flip inc.
        inc = Sign( -inc)
        
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
            #debug("value went below 0 on an unsigned add!")
            
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
        #debug("A is now: " + self.makebin(self.A))
        #debug("Status is now: " + self.makebin(self.PS))
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
         
    def INC(self, val, writer):
        #increment memory
        val += 1
        val &= 0xFF
        if val == 0:
            self.zero = 1
        else:
            self.zero = 0
            
        self.negative = val >> 7
        writer(val)
        self.cycles += 2
    
    def DEC(self, val, writer):
        #decrement memory
        val -= 1
        if val < 0:
            val = 0xFF
            
        if val == 0:
            self.zero = 1
        else:
            self.zero = 0
            
        self.negative = val >> 7
        writer(val)
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
        self.brk = 1
        self.PC += 1 # PC incremented 2, but already +1 from the step().
        #push PC PS onto stack
        self.write(self.S + 0x100, getHigh(self.PC, 8))
        self.S -= 1
        self.write(self.S + 0x100, getLow(self.PC, 8))
        self.S -= 1
        self.write(self.S + 0x100, self.PS)
        self.S -= 1
        self.int_disable = 1
        self.PC = ((self.read(0xFFFF) << 8) + self.read(0xFFFE))
        self.cycles += 7
        
        
    def RTI(self):
        self.S += 1        
        self.PS = self.read(self.S + 0x100)
        self.S += 1
        self.PC = self.read(self.S + 0x100)
        self.S += 1
        self.PC += self.read(self.S + 0x100) << 8
        self.cycles += 6
        
        
    def NOP(self):
        self.cycles += 2
        
    def JPA(self):
        #Absolute Jump
        self.PC = (self.read(self.PC) + (self.read(self.PC+1) << 8))
        self.cycles += 3
        
    def JPI(self):
        #Indirect Jump
        self.PC = (self.read(self.PC) + (self.read(self.PC+1) << 8))
        self.PC = (self.read(self.PC) + (self.read(self.PC+1) << 8))
        self.cycles += 5
        
    def JSR(self):
        self.PC += 1# PC incremented 2, but already +1 from the step().
        self.write(self.S + 0x100, getHigh(self.PC,  8))
        self.S -= 1
        self.write(self.S + 0x100, getLow(self.PC, 8))
        self.S -= 1
        self.PC = (self.read(self.PC-1) + (self.read(self.PC) << 8))
        self.cycles += 6
        
    def RTS(self):
        self.S += 1
        print "firstread: ", self.read(self.S + 0x100)
        self.PC = self.read(self.S + 0x100) 
        self.S += 1
        print "second: ", self.read(self.S + 0x100)
        self.PC += self.read(self.S + 0x100)<< 8
        self.PC += 1
        self.cycles += 6
    
        
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
