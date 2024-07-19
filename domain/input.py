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
