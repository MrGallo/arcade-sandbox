import arcade
from dataclasses import dataclass
from pymunk.vec2d import Vec2d
from arcade.arcade_types import Color
import random


WIDTH = 640
HEIGHT = 480


@dataclass
class Ball:
    position: Vec2d = Vec2d(0, 0)
    velocity: Vec2d = Vec2d(0, 0)
    radius: int = 20
    color: Color = arcade.color.BLACK

    def draw(self):
        arcade.draw_circle_filled(self.position.x, self.position.y, self.radius, self.color)
        return

    def update(self):
        self.position += self.velocity

balls = []
for _ in range(100):
    x = random.randrange(WIDTH)
    y = random.randrange(HEIGHT)
    dx = random.randrange(-5, 5)
    dy = random.randrange(-5, 5)
    radius = random.randrange(10, 30)
    color = random.randrange(256), random.randrange(256), random.randrange(256)
    balls.append(Ball(position=Vec2d(x, y), velocity=Vec2d(dx, dy), radius=radius, color=color))


def setup():
    arcade.open_window(WIDTH, HEIGHT, "My Arcade Game")
    arcade.set_background_color(arcade.color.WHITE)
    arcade.schedule(draw, 1/80)

    # Override arcade window methods
    window = arcade.get_window()
    window.on_key_press = on_key_press
    window.on_key_release = on_key_release

    arcade.run()


def draw(delta_time):

    for ball in balls:
        ball.update()

    arcade.start_render()

    for ball in balls:
        ball.draw()


def on_key_press(key, modifiers):
    pass


def on_key_release(key, modifiers):
    pass


def on_mouse_press(x, y, button, modifiers):
    pass


if __name__ == '__main__':
    setup()
