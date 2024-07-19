from abc import ABC

import pyglet


class CPU(pyglet.window.Window, ABC):
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
        self.stack = [16]  # stack pointer to the address of the topmost element

    def on_key_press(self, symbol, modifiers):
        pass

    def on_key_release(self, symbol, modifiers):
        pass
