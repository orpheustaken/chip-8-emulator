import logging

import pyglet


# TODO: there are more abstract methods from pyglet's superclass to be implemented
class Window(pyglet.window.Window):
    def __init__(self, width, height, title, keys, display_buffer, key_inputs):
        super().__init__(width, height, title)

        self.display_buffer = display_buffer
        self.key_inputs = key_inputs

        # self.label = pyglet.text.Label(
        #     "CHIP-8 Emulator",
        #     font_name="Roboto",
        #     font_size=12,
        #     x=self.width // 2,
        #     y=self.height // 1.1,
        #     anchor_x="center",
        #     anchor_y="center",
        # )

        # both should false by default
        self.should_draw = False
        self.key_wait = False

        # pseudo-pixelwise drawing with 10x10 boxes
        self.pixel = pyglet.image.SolidColorImagePattern(color=(255, 255, 255, 255)).create_image(10, 10)
        self.buzz = pyglet.resource.media('assets/buzz.wav', streaming=False)

        # "pixel" buffer
        self.batch = pyglet.graphics.Batch()
        self.sprites = []

        # fills each output pixel in a batch
        for i in range(0, 2048):
            self.sprites.append(pyglet.sprite.Sprite(self.pixel, batch=self.batch))

        self.KEY_MAP = {
            pyglet.window.key._1: list(keys.values())[0],
            pyglet.window.key._2: list(keys.values())[1],
            pyglet.window.key._3: list(keys.values())[2],
            pyglet.window.key._4: list(keys.values())[3],
            pyglet.window.key.Q: list(keys.values())[4],
            pyglet.window.key.W: list(keys.values())[5],
            pyglet.window.key.E: list(keys.values())[6],
            pyglet.window.key.R: list(keys.values())[7],
            pyglet.window.key.A: list(keys.values())[8],
            pyglet.window.key.S: list(keys.values())[9],
            pyglet.window.key.D: list(keys.values())[10],
            pyglet.window.key.F: list(keys.values())[11],
            pyglet.window.key.Z: list(keys.values())[12],
            pyglet.window.key.X: list(keys.values())[13],
            pyglet.window.key.C: list(keys.values())[14],
            pyglet.window.key.V: list(keys.values())[15],
        }

    def on_draw(self):
        if self.should_draw:
            self.clear()
            # self.label.draw()

            logging.debug("Window: entering drawing loop")
            for i in range(0, 2048):
                if self.display_buffer[i] == 1:
                    if self.display_buffer[i] == 1:
                        self.sprites[i].x = (i % 64) * 10
                        self.sprites[i].y = 310 - ((i / 64) * 10)
                        self.sprites[i].batch = self.batch
                else:
                    self.sprites[i].batch = None

            # draw in batches
            self.batch.draw()
            self.flip()
            self.should_draw = False

    def on_close(self):
        pyglet.app.exit()
        return super().on_close()

    def on_key_press(self, symbol, modifiers):

        logging.info("Key pressed: " + hex(symbol))
        if symbol in self.KEY_MAP.keys():
            self.key_inputs[self.KEY_MAP[symbol]] = 1
            if self.key_wait:
                self.key_wait = False
        else:
            super().on_key_press(symbol, modifiers)

    def on_key_release(self, symbol, modifiers):
        logging.info("Key released: " + hex(symbol))
        if symbol in self.KEY_MAP.keys():
            self.key_inputs[self.KEY_MAP[symbol]] = 0

    @staticmethod
    def run():
        pyglet.app.run()
