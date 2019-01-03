from space_game.enhanced_sprite import EnhancedSprite
from dataclasses import dataclass
from space_game.powerups import PowerUp
from typing import List


class Meteor(EnhancedSprite):
    @dataclass
    class Color:
        BROWN = "Brown"
        GREY = "Grey"

    @dataclass
    class Size:
        BIG1 = "big1"
        BIG2 = "big2"
        BIG3 = "big3"
        BIG4 = "big4"
        MEDIUM1 = "med1"
        MEDIUM2 = "med2"
        SMALL1 = "small1"
        SMALL2 = "small2"
        TINY1 = "tiny1"
        TINY2 = "tiny2"

    def __init__(self, x: int = 0, y: int = 0, color: str = "Brown", size: str = "med1"):
        self.color = color
        self.size = size
        super().__init__(center_x=x,
                         center_y=y,
                         filename="../assets/space_shooter/PNG/Meteors/" + self.get_filename(),
                         scale=0.8)

    def get_filename(self):
        return f"meteor{self.color}_{self.size}.png"


@dataclass
class Level:
    meteors: List[Meteor]
    powerups: List[PowerUp]


levels = []

level_1_meteors = [
    Meteor(100, 100, size=Meteor.Size.BIG1)
]

level_1 = Level(meteors=level_1_meteors, powerups=[])

levels.append(level_1)
