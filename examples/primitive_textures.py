"""
Arcade runs slowly if you constantly draw primitive shapes to represent
your game sprites. To make it run faster, have arcade create a texture
from a primitive shape and use it as the sprite's texture.
"""
import random
import arcade


WIDTH = 640
HEIGHT = 480

window = arcade.open_window(WIDTH, HEIGHT, "My Arcade Game")

player = arcade.Sprite(center_x=0, center_y=0)

# Set player texture to some created square texture
player.texture = arcade.make_soft_square_texture(40, arcade.color.BLUE, outer_alpha=255)
player.velocity = [1, 1]

# save a coin texture for later use
coin_texture = arcade.make_circle_texture(40, arcade.color.GOLD)

# generate coins
coins = arcade.SpriteList()
for _ in range(100):
    # Get random location and speeds
    x = random.randrange(0, WIDTH)
    y = random.randrange(0, HEIGHT)
    dx = random.randrange(-5, 5)
    dy = random.randrange(-5, 5)

    coin = arcade.Sprite(center_x=x, center_y=y)
    coin.velocity = [dx, dy]

    # set the new coin's texture as the saved texture
    coin.texture = coin_texture
    coins.append(coin)


def setup():
    arcade.set_background_color(arcade.color.WHITE)
    arcade.schedule(update, 1/80)

    arcade.run()


def update(delta_time):
    # player update
    player.update()

    # boundary check
    if player.center_x < 0 or player.center_x > WIDTH:
            player.change_x = -player.change_x

    if player.center_y < 0 or player.center_y > HEIGHT:
        player.change_y = -player.change_y

    # update coins
    for coin in coins:
        coin.update()

        if coin.center_x < 0 or coin.center_x > WIDTH:
            coin.change_x = -coin.change_x

        if coin.center_y < 0 or coin.center_y > HEIGHT:
            coin.change_y = -coin.change_y


@window.event
def on_draw():
    arcade.start_render()
    coins.draw()
    player.draw()


if __name__ == '__main__':
    setup()
