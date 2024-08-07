import logging
import random


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
    def __init__(self, app_output, app_window, app_memory, app_input):
        self.app_output = app_output
        self.app_window = app_window
        self.app_memory = app_memory
        self.app_input = app_input

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

        # store register numbers here for op method access
        self.vx = 0
        self.vy = 0

        # instructions of the CHIP-8 interpreter
        self.funcmap = {
            0x0000: self._0ZZZ,
            0x00E0: self._0ZZ0,
            0x00EE: self._0ZZE,
            0x1000: self._1ZZZ,
            0x2000: self._2ZZZ,
            0x3000: self._3ZZZ,
            0x4000: self._4ZZZ,
            0x5000: self._5ZZZ,
            0x6000: self._6ZZZ,
            0x7000: self._7ZZZ,
            0x8000: self._8ZZZ,
            # 0x8001: self._8ZZ1,  # OR
            # 0x8002: self._8ZZ2,  # AND
            # 0x8003: self._8ZZ3,  # XOR
            # 0x8004: self._8ZZ4,  # ADD
            # 0x8005: self._8ZZ5,  # SUB
            # 0x8006: self._8ZZ6,  # SHR
            # 0x8007: self._8ZZ7,  # SUBN
            # 0x800E: self._8ZZE,  # SHL
            0x8FF0: self._8ZZ0,
            0x8FF1: self._8ZZ1,
            0x8FF2: self._8ZZ2,
            0x8FF3: self._8ZZ3,
            0x8FF4: self._8ZZ4,
            0x8FF5: self._8ZZ5,
            0x8FF6: self._8ZZ6,
            0x8FF7: self._8ZZ7,
            0x8FFE: self._8ZZE,
            0x9000: self._9ZZZ,
            0xA000: self._AZZZ,
            0xB000: self._BZZZ,
            0xC000: self._CZZZ,
            0xD000: self._DZZZ,
            0xE000: self._EZZZ,
            0xE009: self._EZZ9,  # SKP
            0xE00A: self._EZZA,  # SKNP
            0xE00E: self._EZZE,
            0xE001: self._EZZ1,
            0xF000: self._FZZZ,
            0xF00D: self._F00D,  # KEYPAD
            0xF007: self._FZ07,
            0xF00A: self._FZ0A,
            0xF015: self._FZ15,
            0xF018: self._FZ18,
            0xF01E: self._F01E,  # ADD_I
            0xF029: self._F029,  # FONT
            0xF033: self._F033,  # BCD
            0xF055: self._F055,  # STORE
            0xF065: self._F065   # FILL
        }

    #############################################
    #           START OF INSTRUCTIONS           #
    #############################################

    # def _8ZZ1(self):
    #     logging.debug("Sets VX to VX OR VY")
    #     self.gpio[self.vx] |= self.gpio[self.vy]
    #     self.gpio[self.vx] &= 0xFF
    #
    # def _8ZZ2(self):
    #     logging.debug("Sets VX to VX AND VY")
    #     self.gpio[self.vx] &= self.gpio[self.vy]
    #     self.gpio[self.vx] &= 0xFF
    #
    # def _8ZZ3(self):
    #     logging.debug("Sets VX to VX XOR VY")
    #     self.gpio[self.vx] ^= self.gpio[self.vy]
    #     self.gpio[self.vx] &= 0xFF
    #
    # def _8ZZ4(self):
    #     logging.debug("Adds VY to VX; VF is set to 1 when there's a carry, and to 0 when there isn't")
    #     result = self.gpio[self.vx] + self.gpio[self.vy]
    #     self.gpio[0xF] = 1 if result > 0xFF else 0
    #     self.gpio[self.vx] = result & 0xFF
    #
    # def _8ZZ5(self):
    #     logging.debug("Subtracts VY from VX; VF is set to 0 when there's a borrow, and 1 when there isn't")
    #     self.gpio[0xF] = 0 if self.gpio[self.vy] > self.gpio[self.vx] else 1
    #     self.gpio[self.vx] = (self.gpio[self.vx] - self.gpio[self.vy]) & 0xFF
    #
    # def _8ZZ6(self):
    #     logging.debug(
    #         "Shifts VX right by one; VF is set to the value of the least significant bit of VX before the shift")
    #     self.gpio[0xF] = self.gpio[self.vx] & 0x01
    #     self.gpio[self.vx] >>= 1
    #
    # def _8ZZ7(self):
    #     logging.debug("Sets VX to VY minus VX; VF is set to 0 when there's a borrow, and 1 when there isn't")
    #     self.gpio[0xF] = 0 if self.gpio[self.vx] > self.gpio[self.vy] else 1
    #     self.gpio[self.vx] = (self.gpio[self.vy] - self.gpio[self.vx]) & 0xFF
    #
    # def _8ZZE(self):
    #     logging.debug(
    #         "Shifts VX left by one; VF is set to the value of the most significant bit of VX before the shift")
    #     self.gpio[0xF] = (self.gpio[self.vx] & 0x80) >> 7
    #     self.gpio[self.vx] <<= 1
    #     self.gpio[self.vx] &= 0xFF

    def _EZZ9(self):
        logging.debug("Skips the next instruction if the key stored in VX is pressed")
        key = self.gpio[self.vx] & 0xF
        if self.app_input.key_inputs[key] == 1:
            self.pc += 2

    def _EZZA(self):
        logging.debug("Skips the next instruction if the key stored in VX is not pressed")
        key = self.gpio[self.vx] & 0xF
        if self.app_input.key_inputs[key] == 0:
            self.pc += 2

    def _F00D(self):
        logging.debug("Sets VX to the value of the delay timer")
        self.gpio[self.vx] = self.delay_timer

    def _F01E(self):
        logging.debug("Adds VX to I; VF is set to 1 if overflow, 0 otherwise")
        self.index += self.gpio[self.vx]
        self.gpio[0xF] = 1 if self.index > 0xFFF else 0
        self.index &= 0xFFF

    def _F029(self):
        logging.debug("Sets I to the location of the sprite for the character in VX")
        self.index = (self.gpio[self.vx] * 5) & 0xFFF

    def _F033(self):
        logging.debug("Stores the binary-coded decimal representation of VX")
        value = self.gpio[self.vx]
        self.app_memory.memory[self.index] = value // 100
        self.app_memory.memory[self.index + 1] = (value // 10) % 10
        self.app_memory.memory[self.index + 2] = value % 10

    def _F055(self):
        logging.debug("Stores V0 to VX in memory starting at address I")
        for i in range(self.vx + 1):
            self.app_memory.memory[self.index + i] = self.gpio[i]
        self.index += self.vx + 1

    def _F065(self):
        logging.debug("Fills V0 to VX with values from memory starting at address I")
        for i in range(self.vx + 1):
            self.gpio[i] = self.app_memory.memory[self.index + i]
        self.index += self.vx + 1

    def _0ZZZ(self):
        extracted_op = self.opcode & 0xF0FF
        try:
            self.funcmap[extracted_op]()
            logging.debug("Found opcode: %X" % self.opcode)
        except KeyError:
            logging.error("Unknown instruction: %X" % self.opcode)

    def _0ZZ0(self):
        logging.debug("Clears the screen")
        self.app_output.display_buffer = [0] * 64 * 32  # 64*32
        self.app_window.should_draw = True

    # to return from a subroutine, pop the topmost address from the stack
    def _0ZZE(self):
        logging.debug("Returns from subroutine")
        self.pc = self.stack.pop()

    # to perform a jump, simply set the program counter to the address of the next instruction
    # it will be performed in the next cycle
    def _1ZZZ(self):
        logging.debug("Jumps to address NNN")
        self.pc = self.opcode & 0x0FFF

    def _2ZZZ(self):
        logging.debug("Calls subroutine at NNN")
        self.stack.append(self.pc)
        self.pc = self.opcode & 0x0FFF

    def _3ZZZ(self):
        logging.debug("Skips the next instruction if VX equals NN")
        if self.gpio[self.vx] == (self.opcode & 0x00FF):
            self.pc += 2

    def _4ZZZ(self):
        logging.debug("Skips the next instruction if VX doesn't equal NN")
        if self.gpio[self.vx] != (self.opcode & 0x00FF):
            self.pc += 2

    def _5ZZZ(self):
        logging.debug("Skips the next instruction if VX equals VY")
        if self.gpio[self.vx] == self.gpio[self.vy]:
            self.pc += 2

    def _6ZZZ(self):
        logging.debug("Sets VX to NN")
        self.gpio[self.vx] = self.opcode & 0x00FF

    def _7ZZZ(self):
        logging.debug("Adds NN to VX")
        self.gpio[self.vx] += self.opcode & 0xFF

    def _8ZZZ(self):
        extracted_op = self.opcode & 0xF00F
        extracted_op += 0xFF0
        try:
            self.funcmap[extracted_op]()
        except KeyError:
            logging.error("Unknown instruction: %X" % self.opcode)

    def _8ZZ0(self):
        logging.debug("Sets VX to the value of VY")
        self.gpio[self.vx] = self.gpio[self.vy]
        self.gpio[self.vx] &= 0xFF

    def _8ZZ1(self):
        logging.debug("Sets VX to VX or VY")
        self.gpio[self.vx] |= self.gpio[self.vy]
        self.gpio[self.vx] &= 0xFF

    def _8ZZ2(self):
        logging.debug("Sets VX to VX and VY")
        self.gpio[self.vx] &= self.gpio[self.vy]
        self.gpio[self.vx] &= 0xFF

    def _8ZZ3(self):
        logging.debug("Sets VX to VX xor VY")
        self.gpio[self.vx] ^= self.gpio[self.vy]
        self.gpio[self.vx] &= 0xFF

    def _8ZZ4(self):
        logging.debug(
            "Adds VY to VX"
            "VF is set to 1 when there's a carry, and to 0 when there isn't"
        )
        if self.gpio[self.vx] + self.gpio[self.vy] > 0xFF:
            self.gpio[0xF] = 1
        else:
            self.gpio[0xF] = 0
        self.gpio[self.vx] += self.gpio[self.vy]
        self.gpio[self.vx] &= 0xFF

    def _8ZZ5(self):
        logging.debug(
            "VY is subtracted from VX"
            "VF is set to 0 when there's a borrow, and 1 when there isn't"
        )
        if self.gpio[self.vy] > self.gpio[self.vx]:
            self.gpio[0xF] = 0
        else:
            self.gpio[0xF] = 1
        self.gpio[self.vx] = self.gpio[self.vx] - self.gpio[self.vy]
        self.gpio[self.vx] &= 0xFF

    def _8ZZ6(self):
        logging.debug(
            "Shifts VX right by one"
            "VF is set to the value of the least significant bit of VX before the shift"
        )
        self.gpio[0xF] = self.gpio[self.vx] & 0x0001
        self.gpio[self.vx] = self.gpio[self.vx] >> 1

    def _8ZZ7(self):
        logging.debug(
            "Sets VX to VY minus VX"
            "VF is set to 0 when there's a borrow, and 1 when there isn't"
        )
        if self.gpio[self.vx] > self.gpio[self.vy]:
            self.gpio[0xF] = 0
        else:
            self.gpio[0xF] = 1
        self.gpio[self.vx] = self.gpio[self.vy] - self.gpio[self.vx]
        self.gpio[self.vx] &= 0xFF

    def _8ZZE(self):
        logging.debug(
            "Shifts VX left by one"
            "VF is set to the value of the most significant bit of VX before the shift"
        )
        self.gpio[0xF] = (self.gpio[self.vx] & 0x00F0) >> 7
        self.gpio[self.vx] = self.gpio[self.vx] << 1
        self.gpio[self.vx] &= 0xFF

    def _9ZZZ(self):
        logging.debug("Skips the next instruction if VX doesn't equal VY")
        if self.gpio[self.vx] != self.gpio[self.vy]:
            self.pc += 2

    def _AZZZ(self):
        logging.debug("Sets I to the address NNN")
        self.index = self.opcode & 0x0FFF

    def _BZZZ(self):
        logging.debug("Jumps to the address NNN plus V0")
        self.pc = (self.opcode & 0x0FFF) + self.gpio[0]

    def _CZZZ(self):
        logging.debug("Sets VX to a random number and NN")
        r = int(random.random() * 0xFF)
        self.gpio[self.vx] = r & (self.opcode & 0x00FF)
        self.gpio[self.vx] &= 0xFF

    def _DZZZ(self):
        logging.debug("Draws sprites to the output")

        self.gpio[0xf] = 0
        x = self.gpio[self.vx] & 0xff
        y = self.gpio[self.vy] & 0xff
        height = self.opcode & 0x000f

        for row in range(height):
            curr_row = self.app_memory.memory[row + self.index]
            pixel_offset = 0
            while pixel_offset < 8:
                loc = x + pixel_offset + ((y + row) * 64)
                pixel_offset += 1
                if (y + row) >= 32 or (x + pixel_offset - 1) >= 64:
                    # ignore pixels outside the screen
                    continue
                mask = 1 << 8 - pixel_offset
                curr_pixel = (curr_row & mask) >> (8 - pixel_offset)
                self.app_output.display_buffer[loc] ^= curr_pixel
                if self.app_output.display_buffer[loc] == 0:
                    self.gpio[0xf] = 1
                else:
                    self.gpio[0xf] = 0

        self.app_window.should_draw = True

    def _EZZZ(self):
        extracted_op = self.opcode & 0xF00F
        try:
            self.funcmap[extracted_op]()
        except KeyError:
            logging.error("Unknown instruction: %X" % self.opcode)

    def _EZZE(self):
        logging.debug("Skips the next instruction if the key stored in VX is pressed")
        key = self.gpio[self.vx] & 0xF
        if self.app_input.key_inputs[key] == 1:
            self.pc += 2

    def _EZZ1(self):
        logging.debug(
            "Skips the next instruction if the key stored in VX isn't pressed"
        )
        key = self.gpio[self.vx] & 0xF
        if self.app_input.key_inputs[key] == 0:
            self.pc += 2

    def _FZZZ(self):
        extracted_op = self.opcode & 0xF0FF
        try:
            self.funcmap[extracted_op]()
        except KeyError:
            logging.error("Unknown instruction: %X" % self.opcode)

    def _FZ07(self):
        logging.debug("Sets VX to the value of the delay timer")
        self.gpio[self.vx] = self.delay_timer

    def _FZ0A(self):
        logging.debug("A key press is awaited, and then stored in VX")
        ret = self.app_input.get_key()
        if ret >= 0:
            self.gpio[self.vx] = ret
        else:
            self.pc -= 2

    def _FZ15(self):
        logging.debug("Sets the delay timer to VX")
        self.delay_timer = self.gpio[self.vx]

    def _FZ18(self):
        logging.debug("Sets the sound timer to VX")
        self.sound_timer = self.gpio[self.vx]

    def _FZ1E(self):
        logging.debug("Adds VX to I" "if overflow, vf = 1")
        self.index += self.gpio[self.vx]
        if self.index > 0xFFF:
            self.gpio[0xF] = 1
            self.index &= 0xFFF
        else:
            self.gpio[0xF] = 0

    def _FZ29(self):
        logging.debug("Set index to point to a character")
        # sets I to the location of the sprite for the character in VX
        # characters 0-F (in hexadecimal) are represented by a 4x5 font
        self.index = (5 * (self.gpio[self.vx])) & 0xFFF

    def _FZ33(self):
        logging.debug("Store a number as BCD")
        # stores the binary-coded decimal representation of VX, with the
        # most significant of three digits at the address in I, the middle
        # digit at I plus 1, and the least significant digit at I plus 2
        self.app_memory.memory[self.index] = self.gpio[self.vx] / 100
        self.app_memory.memory[self.index + 1] = (self.gpio[self.vx] % 100) / 10
        self.app_memory.memory[self.index + 2] = self.gpio[self.vx] % 10

    def _FZ55(self):
        logging.debug("Stores V0 to VX in memory starting at address I")
        for i in range(self.vx):
            self.app_memory.memory[self.index + i] = self.gpio[i]
        self.index += self.vx + 1

    def _FZ65(self):
        logging.debug("Fills V0 to VX with values from memory starting at address I")
        for i in range(self.vx):
            self.gpio[i] = self.app_memory.memory[self.index + i]
        self.index += self.vx + 1

    #############################################
    #            END OF INSTRUCTIONS            #
    #############################################

    def cycle(self):
        logging.debug("Current opcode: %X" % self.opcode)

        # each opcode in CHIP8 is 2 bytes long
        # the program counter points to the current opcode to be processed
        # after getting the op and processing it, the program counter increments by 2 bytes
        # then the process repeats until the program ends

        self.opcode = (self.app_memory.memory[self.pc] << 8) | self.app_memory.memory[self.pc + 1]

        self.vx = (self.opcode & 0x0F00) >> 8
        self.vy = (self.opcode & 0x00F0) >> 4

        self.pc += 2

        # CHIP-8 opcodes are usually in the format XXXX
        # usually instructions can be deciphered from its first (leftmost) nibble
        # we extract the op with a bitwise AND, and look it up in our function map (self.funcmap)
        # if the instruction isn't there, then just raise an error

        # NOTE: self.pc is incremented BEFORE cycle(), so any modifications to it (e.g. in jumps) are retained

        # check ops, lookup and execute
        extracted_op = self.opcode & 0xF000
        try:
            # call the associated method
            self.funcmap[extracted_op]()
        except KeyError:
            logging.error("Unknown instruction: %X" % self.opcode)

        # decrement timers
        if self.delay_timer > 0:
            self.delay_timer -= 1
        if self.sound_timer > 0:
            self.sound_timer -= 1

        if self.sound_timer != 0:
            self.app_window.buzz.play()
