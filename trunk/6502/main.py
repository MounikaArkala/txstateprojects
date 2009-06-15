import CPU
from rom_load import Rom
from errors import *

if __name__ == "__main__":
    rom = Rom("10-Yard Fight (U).nes")
    if rom.mapper != 0:
        raise UnsupportedMapperError("Only mapper 0 (no mapper) is implemented currently, your mapper was %s." % rom.mapper)

    # initialize the CPU, load the ROM

    #initialize the PPU, load the VRAM

    #load the GUI

    #start the CPU execution.
