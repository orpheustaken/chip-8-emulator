# memory map

# +---------------+= 0xFFF (4095) end of Chip-8 RAM
# |               |
# |               |
# |               |
# |               |
# |               |
# | 0x200 to 0xFFF|
# |     Chip-8    |
# | Program / Data|
# |     Space     |
# |               |
# |               |
# |               |
# +- - - - - - - -+= 0x600 (1536) start of ETI 660 Chip-8 programs
# |               |
# |               |
# |               |
# +---------------+= 0x200 (512) start of most Chip-8 programs
# | 0x000 to 0x1FF|
# | Reserved for  |
# |  interpreter  |
# +---------------+= 0x000 (0) start of Chip-8 RAM

class Memory:
    def __init__(self):
        # CHIP-8 supports 4kb of ram
        # from location 0x000 (0) to 0xFFF (4095)
        self.memory = [0] * 4096  # max 4096 bytes
