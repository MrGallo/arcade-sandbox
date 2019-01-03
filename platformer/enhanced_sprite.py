from typing import Sequence
import arcade
from pymunk.vec2d import Vec2d


class EnhancedSprite(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.velocity = Vec2d(0, 0)
        self.position = Vec2d(self.center_x, self.center_y)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, vec):
        self._position = Vec2d(*vec)

    @property
    def velocity(self):
        return self._velocity

    @velocity.setter
    def velocity(self, vec):
        self._velocity = Vec2d(*vec)
