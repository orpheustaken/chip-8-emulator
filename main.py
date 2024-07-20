import sys
import os

from domain.cpu import CPU
from domain.font import Font
from domain.input import Input
from domain.memory import Memory
from domain.output import Output
from domain.window import Window


class Main:
    def __init__(self):
        app_cpu = CPU()
        app_font = Font()
        app_input = Input()
        app_memory = Memory()
        app_output = Output()
        app_window = Window(800, 600, "CHIP-8")

        self.load_rom(sys.argv[1])
        self.load_fonts()

        while not self.has_exit:
            app_window.dispatch_events()
            app_cpu.cycle()
            app_window.run()

    @staticmethod
    def load_rom(rom):
        # if os.path.exists(rom):
        pass

    def load_fonts(self):
        pass

    def has_exit(self):
        pass

    @staticmethod
    def run():
        Window.run()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("ROM must be provided to be run by the CHIP-8 interpreter")
        print("Usage: main.py <rom_path>")
        exit(1)

    app = Main()
    app.run()
