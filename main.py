import sys

from domain.cpu import CPU
from domain.font import Font
from domain.input import Input
from domain.memory import Memory
from domain.output import Output


class Main:
    def __init__(self):
        self.initialize()
        self.load_rom(sys.argv[1])
        self.load_fonts
        while not self.has_exit:
            self.dispatch_events()
            self.cycle()
            self.draw()

    def initialize(self):
        self.clear()
        cpu = CPU()
        font = Font()
        key_input = Input()
        memory = Memory()
        output = Output()

    def load_rom(self):
        pass

    def load_fonts(self):
        pass

    def dispatch_events(self):
        pass

    # TODO: move to CPU class?
    def cycle(self):
        pass

    # TODO: move draw to Output class?
    def draw(self):
        pass

    def has_exit(self):
        pass

    # clear pyglet window
    def clear(self):
        pass
