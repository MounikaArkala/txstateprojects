class Interrupt(object):

    def __init__(self, t="NMI"):
        self.type = t

        
class Register(object):

    def __init__(self, val, size=8):
        self.val = val
        self.size = size
            
    def getLow(self, num_bits):
        return self.val & (2**num_bits - 1)
        # eg. for 16, 8 will yield (self.val & 0000000011111111)
    
    def getHigh(self, num_bits):
        return self.val & ((2**self.size - 1) - (2**(self.size-num_bits) - 1))
        # eg. for 16, 8 will yield self.val & 1111111100000000

class UnsignedRegister(Register):
    
    def add(self, val):
        """ add a value to the register.  returns a set of flags (zero, overflow)"""
        self.val += val
        zero = False
        overflow = False
        
        if self.val > 2**self.size:
            self.val -= 2**self.size
            overflow = True
        if self.val == 0:
            zero = True
            
        return (overflow, zero)



class c6502(object):

    def getStatus(self):
        return (self.negative    << 7) + \
               (self.overflow    << 6) + \
               0x20                    + \
               (self.brk         << 4) + \
               (self.decimal     << 3) + \
               (self.int_disable << 2) + \
               (self.zero        << 1) + \
               self.carry

    PS = property(getStatus) # processor status

    def __init__(self):

        self.X  = UnsignedRegister(0)
        self.Y  = UnsignedRegister(0)
        self.S  = UnsignedRegister(0) # stack pointer
        self.A  = UnsignedRegister(0) #accumulator
        self.PC = UnsignedRegister(0,16)

        self.negative    = 0
        self.overflow    = 0
        self.carry       = 0
        self.zero        = 0
        self.int_disable = 0
        self.decimal     = 0
        self.brk         = 0
        self.cycles      = 0
        
        self.clear_memory()

    def clear_memory(self):
        self.memory = [0]*8000

    def step(self):
        opcode = self.memory[self.PC]
        if opcode == 0x18:
            self.CLC()
            

    #OPCODES

 

    #Status Register Operations - Set or clear a flag in the status register. 
    def CLC(self):
        self.carry = 0
        self.cycles += 2
        
        
#Load / Store Operations - Load a register from memory or stores the contents of a register to memory. 
#Register Transfer Operations - Copy contents of X or Y register to the accumulator or copy contents of accumulator to X or Y register. 
#Stack Operations - Push or pull the stack or manipulate stack pointer using X register. 
#Logical Operations - Perform logical operations on the accumulator and a value stored in memory. 
#Arithmetic Operations - Perform arithmetic operations on registers and memory. 
#Increments / Decrements - Increment or decrement the X or Y registers or a value stored in memory. 
# Shifts - Shift the bits of either the accumulator or a memory location one bit to the left or right. 
 #Jumps / Calls - Break sequential execution sequence, resuming from a specified address. 
 #Branches - Break sequential execution sequence, resuming from a specified address, if a condition is met. The condition involves examining a specific bit in the status register.
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
