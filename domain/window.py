import logging

import pyglet

from pyglet import shapes


# TODO: there are more abstract methods from pyglet's superclass to be implemented
class Window(pyglet.window.Window):
    def __init__(self, width, height, title, keys, display_buffer):
        super().__init__(width, height, title)

        self.display_buffer = display_buffer

        self.label = pyglet.text.Label(
            "CHIP-8 Emulator",
            font_name="Roboto",
            font_size=12,
            x=self.width // 2,
            y=self.height // 1.1,
            anchor_x="center",
            anchor_y="center",
        )

        # both should false by default
        self.should_draw = False
        self.key_wait = False

        # pseudo-pixelwise drawing with 10x10 boxes
        self.pixel = pyglet.resource.image('assets/pixel.png')
        self.buzz = pyglet.resource.media('assets/buzz.wav', streaming=False)

        # "pixel" buffer
        self.batch = pyglet.graphics.Batch()
        self.sprites = [2048]

        # fills each output pixel in a batch
        logging.debug("__init__: entering drawing loop")
        for i in range(0, 2048):
            # self.sprites.append(pyglet.sprite.Sprite(self.pixel, batch=self.batch))

            display_buffer[i] = 1

            sprite = pyglet.sprite.Sprite(self.pixel, batch=self.batch)
            sprite.x = (i % 64) * 10  # 64 sprites per row, each 10 pixels wide
            sprite.y = (i // 64) * 10  # each new row starts at y = (row number) * 10
            self.sprites.append(sprite)

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
            self.label.draw()

            self.pixel = pyglet.image.SolidColorImagePattern(color=(48, 48, 48, 255)).create_image(10, 10)

            logging.debug("on_draw: entering drawing loop")
            for i in range(0, 2048):
                if self.display_buffer[i] == 1:
                    sprite = pyglet.sprite.Sprite(self.pixel, batch=self.batch)
                    sprite.x = (i % 64) * 10  # 64 sprites per row, each 10 pixels wide
                    sprite.y = (i // 64) * 10  # each new row starts at y = (row number) * 10
                    self.sprites.append(sprite)

            # draw in batches
            self.batch.draw()
            self.flip()
            self.should_draw = False

    def on_close(self):
        pyglet.app.exit()
        return super().on_close()

    def dispatch_events(self):
        pass

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.SPACE:
            logging.debug("Space pressed: Drawing window")
            self.should_draw = True

        if symbol == pyglet.window.key.ENTER:
            logging.debug("Enter pressed: Cleaning window")
            self.clear()

    def on_key_release(self, symbol, modifiers):
        pass

    @staticmethod
    def run():
        pyglet.app.run()
