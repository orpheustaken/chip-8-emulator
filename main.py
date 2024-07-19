import sys


class Main:
    def __init__(self):
        self.initialize()
        self.load_rom(sys.argv[1])
        while not self.has_exit:
            self.dispatch_events()
            self.cycle()
            self.draw()

    def initialize(self):
        pass

    def load_rom(self):
        pass

    def dispatch_events(self):
        pass

    def cycle(self):
        pass

    def draw(self):
        pass

    def has_exit(self):
        pass
