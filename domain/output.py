# display coordinates

# +-------------------+
# | (0, 0)   (63, 0)  |
# |                   |
# | (0, 31)  (63, 31) |
# +-------------------+

class Output:
    def __init__(self):
        # 64x32 monochrome display
        self.display_buffer = [0] * 32 * 64
        # update screen only when needed
        self.should_draw = False
