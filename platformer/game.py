from collections import defaultdict
from dataclasses import dataclass, asdict
import numpy as np
import arcade
from enhanced_sprite import EnhancedSprite


@dataclass(frozen=True)
class Tile:
    DIRT_GRASS: int = 1
    DIRT: int = 4
    BRICK_BROWN: int = 34
    PANEL_BROWN: int = 35
    LADDER_TOP: int = 37
    LADDER_BOT: int = 38
    BRIDGE: int = 39
    BRICK_GRAY: int = 40
    PANEL_GRAY: int = 41
    SAW: int = 44
    DOOR: int = 48

# TODO: wish: Sprites position and velocity are pymunk.Vec2d by default.

class Saw(EnhancedSprite):
    def update(self):
        super().update()
        self.angle += 20
        if self.left < self.boundary_left:
            self.left = self.boundary_left
            self.velocity *= -1
        elif self.right > self.boundary_right:
            self.right = self.boundary_right
            self.velocity *= -1


WIDTH = 1280
HEIGHT = 720
SPRITE_SCALE = 0.75
GRAVITY = 0.8
SPRITE_SPEED = 5
GRID_SIZE = int(arcade.load_texture("../assets/platformer/PNG/Tiles/platformPack_tile034.png").width * SPRITE_SCALE)
keys_pressed = defaultdict(bool)

# Game state
GAME_OVER = 0
GAME_RUNNING = 1
game_state = GAME_RUNNING


platforms = arcade.SpriteList(is_static=True)
ladders = arcade.SpriteList(is_static=True)
saws = arcade.SpriteList(is_static=False)
level_exit: arcade.Sprite


start_x, start_y = 3, 4
player = EnhancedSprite(filename="../assets/platformer/PNG/Characters/platformChar_idle.png",
                        scale=SPRITE_SCALE*0.9,
                        center_x=start_x * GRID_SIZE + GRID_SIZE // 2,
                        center_y=start_y * GRID_SIZE + GRID_SIZE // 2)
w, h = player.width/3, player.height/2
player.points = ((-w, -h), (w, -h), (w, h-23), (-w, h-23))

# TODO: wish: modifying hitbox would be easier. e.g., player.hitbox *= 0.8, to shrink in-place slightly
# TODO: wish: modify hitbox by size. E.g., player.hitbox.top -= 5 or player.hitbox.top = 50 (from middle)


level = np.zeros((HEIGHT//GRID_SIZE, WIDTH//GRID_SIZE+1), dtype=int)
# shape: (14, 15)
level[-1] = Tile.DIRT  # floor row
level[-2] = Tile.DIRT_GRASS
level[-4, 2:6] = Tile.BRICK_BROWN
level[-6, 9:14] = Tile.BRICK_BROWN
level[-6, 14:18] = Tile.BRIDGE
level[-6:-2, 18:20] = Tile.PANEL_GRAY
level[-11, 22] = Tile.LADDER_TOP
level[-10:-2, 22] = Tile.LADDER_BOT
level[-11, 23:] = Tile.PANEL_BROWN
level[-12, -2] = Tile.DOOR

tile_file_template = "../assets/platformer/PNG/Tiles/platformPack_tile{:03d}.png"

# add movable sprites
dummy = arcade.Sprite()
dummy.width = 4*GRID_SIZE/5
dummy.height = 4*GRID_SIZE/5

start_x, start_y = 10, 7
left, right = 9, 20
saw_1 = Saw(filename=tile_file_template.format(Tile.SAW),
            scale=SPRITE_SCALE,
            center_x=start_x*GRID_SIZE + GRID_SIZE//2,
            center_y=start_y*GRID_SIZE + GRID_SIZE//2)
saw_1.boundary_left = left * GRID_SIZE
saw_1.boundary_right = right * GRID_SIZE
saw_1.velocity.x = 2
saw_1.points = dummy.points

start_x, start_y = 15, 6
left, right = 9, 20
saw_2 = Saw(filename=tile_file_template.format(Tile.SAW),
            scale=SPRITE_SCALE,
            center_x=start_x*GRID_SIZE + GRID_SIZE//2,
            center_y=start_y*GRID_SIZE + GRID_SIZE//2)
saw_2.boundary_left = left * GRID_SIZE
saw_2.boundary_right = right * GRID_SIZE
saw_2.velocity.x = -4
saw_2.points = dummy.points

# TODO: wish: after changing the points, they still rotate when the sprite angle changes.

saws.append(saw_1)
saws.append(saw_2)

# add static sprites
for y, row in enumerate(reversed(level)):
    for x, tile_value in enumerate(row):
        if tile_value in asdict(Tile()).values():  # make platform
            tile_sprite = EnhancedSprite(filename=tile_file_template.format(tile_value),
                                         scale=SPRITE_SCALE,
                                         center_x=x*GRID_SIZE + GRID_SIZE//2,
                                         center_y=y*GRID_SIZE + GRID_SIZE//2)

            if tile_value in (Tile.LADDER_TOP, Tile.LADDER_BOT):
                ladders.append(tile_sprite)
            elif tile_value == Tile.DOOR:
                level_exit = tile_sprite
            elif tile_value == Tile.SAW:
                saws.append(tile_sprite)
            else:
                platforms.append(tile_sprite)

# TODO: wish: physics engine platformer accepts player sprite list for multiple players
# TODO: wish: arcade.SpriteList concat with '+' operator
physics_engine = arcade.PhysicsEnginePlatformer(player_sprite=player, platforms=platforms, gravity_constant=GRAVITY)


def setup():
    arcade.open_window(WIDTH, HEIGHT, "My Platformer")
    arcade.set_background_color(arcade.color.SKY_BLUE)
    arcade.schedule(update, 1/80)

    # Override arcade window methods
    window = arcade.get_window()
    window.on_draw = draw
    window.on_key_press = on_key_press
    window.on_key_release = on_key_release

    arcade.run()


def update(delta_time):
    global game_state

    if game_state is GAME_RUNNING:
        if keys_pressed[arcade.key.SPACE]:
            if physics_engine.can_jump():
                player.velocity.y = 15

        if keys_pressed[arcade.key.A]:  # left
            player.velocity.x = -SPRITE_SPEED
        elif keys_pressed[arcade.key.D]:  # right
            player.velocity.x = SPRITE_SPEED
        else:
            player.velocity.x *= 0.8

        ladder_collisions = arcade.check_for_collision_with_list(player, ladders)
        if ladder_collisions and keys_pressed[arcade.key.W]:
            player.velocity.y = SPRITE_SPEED
        elif ladder_collisions and keys_pressed[arcade.key.S]:
            player.velocity.y = -SPRITE_SPEED
        elif ladder_collisions:
            player.velocity.y = GRAVITY

        if ladder_collisions and keys_pressed[arcade.key.SPACE]:
            player.velocity.y = 15

        if arcade.check_for_collision(player, level_exit) and keys_pressed[arcade.key.W]:
            print("LEVEL COMPLETE")

        saw_collisions = arcade.check_for_collision_with_list(player, saws)
        if saw_collisions:
            player.velocity.y = 10
            player.velocity.x *= -0.5
            player.angle = 45
            game_state = GAME_OVER

        physics_engine.update()
        saws.update()

    elif game_state is GAME_OVER:
        player.update()
        player.velocity.y += -GRAVITY


def draw():
    arcade.start_render()
    platforms.draw()
    ladders.draw()
    level_exit.draw()
    saws.draw()

    player.draw()

    # TODO: Documentation fix:
    # arcade.draw_xywh_rectangle_filled(bottom_left_x: float, bottom_left_y: float .....)
    if game_state is GAME_OVER:
        try:
            draw.fade += 4
        except AttributeError:
            draw.fade = 1
        arcade.draw_xywh_rectangle_filled(0, 0, WIDTH, HEIGHT, (*arcade.color.BLACK, min(draw.fade, 255)))
        arcade.draw_text("GAME OVER", 0, HEIGHT/2, arcade.color.WHITE, 30, width=WIDTH, align="center")


def on_key_press(key, modifiers):
    keys_pressed[key] = True


def on_key_release(key, modifiers):
    keys_pressed[key] = False


def on_mouse_press(x, y, button, modifiers):
    pass


if __name__ == '__main__':
    setup()
