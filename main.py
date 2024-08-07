import sys
import os
import logging

from domain.cpu import CPU
from domain.font import Font
from domain.input import Input
from domain.memory import Memory
from domain.output import Output
from domain.window import Window

logging.basicConfig(
    filename="chip-8-emulator.log",
    filemode="w",  # 'a' for append, 'w' for overwrite
    level=logging.INFO,  # level of logging
    format="%(asctime)s - %(levelname)s - %(filename)s - %(lineno)d - %(funcName)s - %(message)s",
)


class Main:
    def __init__(self):
        self.app_font = Font()
        self.app_input = Input()
        self.app_memory = Memory()
        self.app_output = Output()
        self.app_window = Window(640, 320, "CHIP-8", self.app_input.key_map, self.app_output.display_buffer,
                                 self.app_input.key_inputs)
        self.app_cpu = CPU(self.app_output, self.app_window, self.app_memory, self.app_input)

        self.load_rom(sys.argv[1])
        self.load_fonts()

        while not self.app_window.has_exit:
            self.app_window.dispatch_events()
            self.app_cpu.cycle()
            self.app_window.on_draw()

    def load_rom(self, rom):
        if os.path.isfile(rom):
            logging.info("Loading ROM image %s into the emulator's memory..." % rom)

            with open(rom, "rb") as file:
                rom_binary = file.read()

            # TODO: add try-catch for memory limit reached
            for i in range(len(rom_binary)):
                self.app_memory.memory[i + 0x200] = rom_binary[i]

            logging.info("ROM image loaded successfully")
        else:
            print("ROM image path is not valid")
            exit(2)

    def load_fonts(self):
        logging.info("Loading fonts into the emulator's memory")

        for font in self.app_font.fonts.values():
            self.app_memory.memory.append(font)

    def run(self):
        if not self.app_window.has_exit:
            logging.info("Starting CHIP-8 window...")
        else:
            logging.info("Stopping CHIP-8 Emulator")

        self.app_window.run()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("ROM image must be provided to be run by the CHIP-8 interpreter")
        print("Usage: main.py <rom_img_path>")
        exit(1)

    app = Main()
    app.run()
