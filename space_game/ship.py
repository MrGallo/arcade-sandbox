from pymunk.vec2d import Vec2d
from space_game.enhanced_sprite import EnhancedSprite
import time

class Ship(EnhancedSprite):
    class Thrust:
        CW = -1
        CCW = 1
        FORWARD = 0.1
        BACKWARD = -0.05

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rotation_rate = 3
        self.lazer_last_shot_time = 0
        self.lazer_fire_delay = 0.5  # seconds

    def thrust_longitudinal(self, direction):
        self.velocity += Vec2d(0, 1).rotated_degrees(self.angle) * direction

    def thrust_rotational(self, direction):
        self.angle += self.rotation_rate * direction

    def fire_lazer(self):
        if time.time() > self.lazer_last_shot_time + self.lazer_fire_delay:
            self.lazer_last_shot_time = time.time()
            lazer = LazerBolt("../assets/space_shooter/PNG/Lasers/laserRed01.png", 0.5)
            lazer.position = Vec2d(self.position)
            lazer.velocity = Vec2d(0, 7).rotated_degrees(self.angle)
            lazer.angle = self.angle
            return lazer


class LazerBolt(EnhancedSprite):
    def update(self):
        super().update()
