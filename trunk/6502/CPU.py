
class Register(object):

    def __init__(self, val, size=8):
        self.val = val
        self.size = size

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
            
    def getLow(self, num_bits):
        """ Tested, works! """
        return self.val & (2**num_bits - 1)
        # eg. for 16, 8 will yield (self.val & 0000000011111111)
    
    def getHigh(self, num_bits):
        """ Tested, works! """
        return self.val & ((2**self.size - 1) - (2**(self.size-num_bits) - 1))
        # eg. for 16, 8 will yield self.val & 1111111100000000


class c6502(object):

    def __init__(self):

        self.X   = UnsignedRegister(0)
        self.Y   = UnsignedRegister(0)
        self.S   = UnsignedRegister(0)
        self.ACC = UnsignedRegister(0)
        self.PC  = UnsignedRegister(0,16)
        

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
