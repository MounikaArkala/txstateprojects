
import CPU


class RicohCPU(CPU.c6502):
    
    
    def write(self, address, val): #perform mirroring
        if address < 0x2000:
            print "first mirrored range"
            for i in range(4):
                print "writing to: ", hex((address % 0x0800) + (0x0800 * i))
                self.memory[(address % 0x0800) + (0x0800 * i)] = val
        elif address >= 0x2000 and address < 0x4000:
            print "second mirrored range"
            target = address % 8
            target += 0x2000
            for i in range(1024):
                self.memory[target + (8 * i)] = val
                print "writing to: ", hex(target + (8 * i))
        

if __name__ == "__main__":
    x = RicohCPU()
    x.write(0x2000, 0x25)
    print x.memory[2005]