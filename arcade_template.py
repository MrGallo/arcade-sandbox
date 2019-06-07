import arcade


WIDTH = 640
HEIGHT = 480

window = arcade.open_window(WIDTH, HEIGHT, "My Arcade Game")


def setup():
    arcade.set_background_color(arcade.color.WHITE)
    arcade.schedule(update, 1/80)

    arcade.run()


def update(delta_time):
    pass


@window.event
def on_draw():
    arcade.start_render()


@window.event
def on_key_press(key, modifiers):
    pass


@window.event
def on_key_release(key, modifiers):
    pass


@window.event
def on_mouse_press(x, y, button, modifiers):
    pass


@window.event
def on_mouse_release(x, y, button, modifiers):
    pass


if __name__ == '__main__':
    setup()
