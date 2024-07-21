# the original implementation of the Chip-8 language includes 36 different instructions
# including math, graphics, and flow control functions

# super Chip-48 added 10 instructions, for a total of 46
# all instructions are 2 bytes long and are stored most-significant-byte first

# in these listings, the following variables are used:

# nnn or addr - A 12-bit value, the lowest 12 bits of the instruction
# n or nibble - A 4-bit value, the lowest 4 bits of the instruction
# x - A 4-bit value, the lower 4 bits of the high byte of the instruction
# y - A 4-bit value, the upper 4 bits of the low byte of the instruction
# kk or byte - An 8-bit value, the lowest 8 bits of the instruction


class CPU:
    def __init__(self):
        super().__init__()
        # 16 general purpose 8-bit registers, also referred as Vx where x is a hexadecimal digit (0 through F)
        self.gpio = [0] * 16

        # delay and timer registers
        self.sound_timer = 0
        self.delay_timer = 0

        # index register is generally used to store memory addresses
        # so only the lowest (rightmost) 12 bits are usually used
        self.index = 0  # 16-bit index register

        # program counter starts from memory address 0x200 (512)
        # first 512 bytes, from 0x000 to 0x1FF, are where the original interpreter was located
        self.pc = 0x200  # 16-bit program counter register
        self.opcode = 0

        # stack pointer to the address of the topmost element
        self.stack = [16]

    def cycle(self):
        pass
