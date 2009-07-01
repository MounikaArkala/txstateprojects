

class Rom(object):

    def __init__(self, f, validate=False, chk_header=True):
        """ set validate to True if you want to run checks."""
        
        data = open(f, "rb").read()
        if data[0:4] != "NES" + chr(26):
            if chk_header:
                raise NESHeaderError
        data = [ord(i) for i in data]
        
        if data[6] & 0x0D != 0: # bit 1, 2, 3 must be 0s.
            if validate:
                raise ReservedBitsError
        if data[9] & 0xFE != 0: # bits 1-7 must be 0s.
            if validate:
                raise ReservedBitsError
        if sum(data[10:16]) != 0:
            if validate:
                raise ReservedBitsError
            
        self.rom_banks   = data[4]
        self.vrom_banks  = data[5]
        self.vmirror     = data[6] & 0x01 # bit 0, vertical / horizontal mirroring
        self.batt_ram    = data[6] & 0x02 # bit 1, battery-backed RAM at $6000-$7FFF
        self.has_trainer = data[6] & 0x04 # bit 2, 512-byte trainer at $7000-$71FF
        self.four_screen = data[6] & 0x08 # bit 3, four-screen VRAM layout.
        self.vs_system   = data[7] & 0x01 # bit 0, vertical / horizontal mirroring
        self.ram         = data[8]
        self.pal         = data[9] & 0x01
        self.mapper      = (data[7] & 0xF0) + (data[6] & 0x0F) # because marat is retarded. or a genius.

        if self.ram == 0: # compatibility with older specs of the .NES format
            self.ram = 1

        startaddr = 16
        if self.has_trainer:
            self.trainer = data[startaddr:startaddr+512]
            startaddr += 512

        temp = data[startaddr:startaddr+self.rom_banks*16384]
        self.rom = [temp[i*16384:(i+1)*16384] for i in range(self.rom_banks)]
        temp = data[startaddr+self.rom_banks*16384:]
        self.vrom = [temp[i*8192:(i+1)*8192] for i in range(self.vrom_banks)]
