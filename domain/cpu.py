from abc import ABC

import pyglet


class CPU(pyglet.window.Window, ABC):
    def __init__(self):
        super().__init__()
        self.gpio = [0] * 16  # 16 8-bit registers
        # delay registers
        self.sound_timer = 0
        self.delay_timer = 0
        self.index = 0  # 16-bit index register
        self.pc = 0  # 16-bit program counter register
        self.stack = []  # stack pointer to the topmost element

    def on_key_press(self, symbol, modifiers):
        pass

    def on_key_release(self, symbol, modifiers):
        pass
