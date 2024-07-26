# keypad layout

# +---+---+---+---+
# | 1 | 2 | 3 | C |
# +---+---+---+---+
# | 4 | 5 | 6 | D |
# +---+---+---+---+
# | 7 | 8 | 9 | E |
# +---+---+---+---+
# | A | 0 | B | F |
# +---+---+---+---+


class Input:
    def __init__(self):
        # 16-key hexadecimal keypad for input
        self.key_inputs = [0] * 16
        self.key_map = {
            "1": 0x1,
            "2": 0x2,
            "3": 0x3,
            "4": 0xC,
            "Q": 0x4,
            "W": 0x5,
            "E": 0x6,
            "R": 0xD,
            "A": 0x7,
            "S": 0x8,
            "D": 0x9,
            "F": 0xE,
            "Z": 0xA,
            "X": 0x0,
            "C": 0xB,
            "V": 0xF,
        }

    def get_key(self):
        for key in self.key_inputs:
            if self.key_inputs[key] == 1:
                return key
        return -1
