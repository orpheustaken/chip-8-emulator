# sprite of number 0 as an example

# +------+----------+------+
# | "0"  |  Binary  |  Hex |
# +------+----------+------+
# | **** | 11110000 | 0xF0 |
# | *  * | 10010000 | 0x90 |
# | *  * | 10010000 | 0x90 |
# | *  * | 10010000 | 0x90 |
# | **** | 11110000 | 0xF0 |
# +------+----------+------+

class Font:
    def __init__(self):
        # sprites in memory for the 16 hexadecimal digits
        # each font character is 8x5 bits, so 5 bytes of memory per character
        self.fonts = []
