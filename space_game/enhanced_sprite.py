import arcade
from pymunk.vec2d import Vec2d


class EnhancedSprite(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._velocity = Vec2d(0, 0)
        self._position = Vec2d(self.center_x, self.center_y)

    def draw(self, debug=False):
        super().draw()
        if debug:
            arcade.draw_polygon_outline(self.points, arcade.color.GREEN, 1)

    @property
    def velocity(self):
        return self._velocity

    @velocity.setter
    def velocity(self, vec):
        self._velocity = Vec2d(*vec)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, vec):
        self._position = Vec2d(*vec)
