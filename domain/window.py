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
