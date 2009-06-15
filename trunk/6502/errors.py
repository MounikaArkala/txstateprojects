""" Main errors"""
class UnsupportedMapperError(Exception):
    """Exception raised when the ROM has an unsupported mapper."""
    def __init__(self, value="No message specified."):
        self.value = value
    def __str__(self):
        return repr(self.value)




""" Rom-parsing-related errors"""

class ReservedBitsError(Exception):
    """Exception raised for errors in checking reserved bits in the NES header during ROM parsing."""
    def __init__(self, value="No message specified."):
        self.value = value
    def __str__(self):
        return repr(self.value)

class NESHeaderError(Exception):
    """Exception raised when the ROM doesn't contain NES^Z tag as the first 4 characters."""
    def __init__(self, value="No message specified."):
        self.value = value
    def __str__(self):
        return repr(self.value)
