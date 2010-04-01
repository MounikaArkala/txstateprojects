"""
TODO: make CPU use a list of MemoryLocaiton objects so that we can deny access to
values that are in the interpreter range without using getters / setters.

class MemoryLocation(object):
    def __init__(self, index, value):
        self.
"""

class CPU(object):
    def __init__(self):
        self.memory = [0] * 0xFFFF
        #TODO: load the characters into memory.
        self.memory
        
        self.screen = [[0] * 0x20 for i in range(0x40)]
        self.screen[3][2]  = 1
        print self.screen
        
        
    def draw(self, surface):
        
        
cpu = CPU()

    