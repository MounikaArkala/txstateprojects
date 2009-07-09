
import CPU
import PPU
import ROMS

class RicohCPU(CPU.c6502):
    
    valid_mappers = [0]
    
    def write(self, address, val): #perform mirroring
        if address < 0x2000:
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
            
    def load_rom(self, location):
        self.rom = ROMS.Rom(location)
        if not self.rom.mapper in self.valid_mappers:
            print "The mapper", self.rom.mapper, "is not currently supported."
        addr = 0x8000
        bank = self.rom.rom[0]
        for byte in bank:
            self.write(addr, byte)
            addr += 1
            #print "writing ", hex(byte), "to address", hex(addr)
        if self.rom.rom_banks > 1:
            bank = self.rom.rom[1]
        #otherwise we'll just load bank 1 into both locations :)
        for byte in bank:
            self.write(addr, byte)
            addr += 1
        if self.rom.vrom_banks > 0:
            addr = 
            bank = self.rom.vrom[0]
            for byte in bank:
                self.PPU.write(addr, byte)
                addr += 1
        
        #load CHR rom into PPU
        
    
    #TODO: make this the __init__ and call parent's __init__!!
    def __init__(self, RomName=None):
        super(RicohCPU, self).__init__()
        self.PPU = PPU.pC202()
        self.PC = 0x8000
        if RomName:
            self.load_rom(RomName)
            self.reset()
            
if __name__ == "__main__":
    x = RicohCPU("TestGame.nes")
    #x.write(0x2000, 0x25)
    while 1:
        for i in xrange(100000):
            x.step()
        print x.cycles
    #print x.memory