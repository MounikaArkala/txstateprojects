"""
TODO: make CPU use a list of MemoryLocaiton objects so that we can deny access to
values that are in the interpreter range without using getters / setters.

class MemoryLocation(object):
    def __init__(self, index, value):
        self.
"""
import config
BYTE = 0x100
WORD = 0x10000

def bin(item, bits):
    return [(item & (1 << (i-1))) >>  i-1 for i in range(bits, 0, -1)]


class Value(object):
    "Contains unsigned integer values, of a specific maximum size (modval)"
    def __init__(self, value=None, modval=BYTE):
        if value == None:
            value = 0
        self.value = abs(value) % modval   
        self.modval = modval
    
    def __set_value(self, value):
        self.value = value % self.modval
    def __get_value(self):
        return self.value
    val = property(__get_value, __set_value)
    
    def __repr__(self):
        return str(self.value)
        
class Byte(Value):
    "An 8-bit unsigned integer."
    def __init__(self, value=None):
        super(Byte, self).__init__(value=value, modval=BYTE)
        
class Word(Value):
    "A 16-bit unsigned integer."
    def __init__(self, value=None):
        super(Word, self).__init__(value=value, modval=WORD)
        

class CPU(object):
    def __init__(self):
        self.memory = [Byte() for i in range(WORD)]
        
        self.regs = [Byte() for i in range(0x10)]
        self.delay = Byte()
        self.sound = Byte()
        self.SP    = Byte()
        
        self.stack = [Word() for i in range(0x10)]
        self.I     =  Word()
        self.PC    =  Word()
        
        self._load_memory(Word(0), config.hexfont)     
        self.clear()
        
    def _load_memory(self, addr, values):
        loc = abs(addr.val) % WORD
        for i in values:
            self.memory[loc].val = i
            loc += 1
            loc %= WORD
            
    def draw(self, sprite, x,y):
        #all sprites are 8 bits wide, and however many bytes tall.
        for v, row in enumerate(sprite):
            for h, pixel in enumerate(bin(row, 8)):
                hloc = (x+h) % len(self.screen)
                vloc = (y+v) % len(self.screen[0])
                if self.screen[hloc][vloc] and pixel:
                    print "flipping bit."
                    self.regs[-1] = 1
                self.screen[hloc][vloc] = self.screen[hloc][vloc] ^ pixel
    
    def clear(self):
        self.screen = [[0] * 0x20 for i in range(0x40)]
        
    

class Display(object):
    def __init__(self, CPU, screen):
        self.cpu = CPU
        self.screen = screen
        
    def update(self):
        self.screen.lock()
        for x, row in enumerate(self.cpu.screen):
            for y, col in enumerate(row):
                color = [(0,0,0), (255,255,255)][col]
                self.screen.fill(color, (x*10,y*10, x*10+10, y*10+10))
        self.screen.unlock()
        


    