class CPU:
    def __init__(self):
        self.gpio = [0]*16  # 16 8-bit registers
        # delay registers
        self.sound_timer = 0
        self.delay_timer = 0
        self.index = 0  # 16-bit index register
        self.pc = 0  # 16-bit program counter register
        self.stack = []  # stack pointer to the topmost element
