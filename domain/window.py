import pyglet

from pyglet import shapes


# TODO: there are more abstract methods from pyglet's superclass to be implemented
class Window(pyglet.window.Window):
    def __init__(self, width, height, title, keys):
        super().__init__(width, height, title)

        # self.label = pyglet.text.Label(
        #     "CHIP-8",
        #     font_name="Roboto",
        #     font_size=36,
        #     x=self.width // 2,
        #     y=self.height // 2,
        #     anchor_x="center",
        #     anchor_y="center",
        # )
        # self.batch = pyglet.graphics.Batch()
        # self.rectangle = shapes.Rectangle(
        #     200, 150, 400, 300, color=(255, 255, 255), batch=self.batch
        # )

        self.should_draw = False
        self.key_wait = False

        # pseudo-pixelwise drawing with 10x10 boxes
        self.pixel = pyglet.resource.image('assets/pixel.png')
        self.buzz = pyglet.resource.media('assets/buzz.wav', streaming=False)

        # "pixel" buffer
        self.batch = pyglet.graphics.Batch()
        self.sprites = []

        for i in range(0, 2048):
            self.sprites.append(pyglet.sprite.Sprite(self.pixel, batch=self.batch))

        self.KEY_MAP = {
            pyglet.window.key._1: keys.values(0),
            pyglet.window.key._2: keys.values(1),
            pyglet.window.key._3: keys.values(2),
            pyglet.window.key._4: keys.values(3),
            pyglet.window.key.Q: keys.values(4),
            pyglet.window.key.W: keys.values(5),
            pyglet.window.key.E: keys.values(6),
            pyglet.window.key.R: keys.values(7),
            pyglet.window.key.A: keys.values(8),
            pyglet.window.key.S: keys.values(9),
            pyglet.window.key.D: keys.values(10),
            pyglet.window.key.F: keys.values(11),
            pyglet.window.key.Z: keys.values(12),
            pyglet.window.key.X: keys.values(13),
            pyglet.window.key.C: keys.values(14),
            pyglet.window.key.V: keys.values(15),
        }

    def on_draw(self):
        if self.should_draw:
            self.clear()
            # self.label.draw()
            # self.batch.draw()

    def on_close(self):
        pyglet.app.exit()
        return super().on_close()

    def dispatch_events(self):
        pass

    def on_key_press(self, symbol, modifiers):
        pass

    def on_key_release(self, symbol, modifiers):
        pass

    @staticmethod
    def run():
        pyglet.app.run()
