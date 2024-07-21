import pyglet

from pyglet import shapes


# TODO: there are more abstract methods from pyglet's superclass to be implemented
class Window(pyglet.window.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.label = pyglet.text.Label(
            "CHIP-8",
            font_name="Roboto",
            font_size=36,
            x=self.width // 2,
            y=self.height // 2,
            anchor_x="center",
            anchor_y="center",
        )
        self.batch = pyglet.graphics.Batch()
        self.rectangle = shapes.Rectangle(
            200, 150, 400, 300, color=(255, 255, 255), batch=self.batch
        )
        # TODO: update screen only when needed
        self.should_draw = True

        self.KEY_MAP = {
            pyglet.window.key._1: 0x1,
            pyglet.window.key._2: 0x2,
            pyglet.window.key._3: 0x3,
            pyglet.window.key._4: 0xC,
            pyglet.window.key.Q: 0x4,
            pyglet.window.key.W: 0x5,
            pyglet.window.key.E: 0x6,
            pyglet.window.key.R: 0xD,
            pyglet.window.key.A: 0x7,
            pyglet.window.key.S: 0x8,
            pyglet.window.key.D: 0x9,
            pyglet.window.key.F: 0xE,
            pyglet.window.key.Z: 0xA,
            pyglet.window.key.X: 0,
            pyglet.window.key.C: 0xB,
            pyglet.window.key.V: 0xF,
        }

    def on_draw(self):
        if self.should_draw:
            self.clear()
            self.label.draw()
            self.batch.draw()

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
