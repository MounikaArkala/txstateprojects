

class pC202(object):    

    def __init__(self):
        
        self.initialize()
    
    def clear_memory(self):
        self.memory = [0]*0x10000

    def initialize(self):
        self.clear_memory() # init memory
        self.cycles = 0     # Cycle Count


    def write(self, address, val): #perform mirroring
        if address < 0x3F00:
            #print "first mirrored range"
            for i in range(4):
                #print "writing to: ", hex((address % 0x0800) + (0x0800 * i))
                self.memory[(address % 0x0800) + (0x0800 * i)] = val
        elif address >= 0x2000 and address < 0x4000:
            #print "second mirrored range"
            target = address % 8
            target += 0x2000
            for i in range(1024):
                self.memory[target + (8 * i)] = val
                #print "writing to: ", hex(target + (8 * i))
        else:
            self.memory[address] = val

    def read(self, addr):
        return self.memory[addr]
