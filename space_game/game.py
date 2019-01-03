import arcade
from pymunk.vec2d import Vec2d
from collections import defaultdict
from space_game.ship import Ship
from space_game.levels import Meteor
from space_game.powerups import PowerUp


WIDTH = 800
HEIGHT = 600
runtime = 0  # in seconds
keys_pressed = defaultdict(bool)
score = 0

background_img = arcade.load_texture("../assets/space_shooter/Backgrounds/blue.png")
player_lazerbolts = arcade.SpriteList()
powerups = arcade.SpriteList()
meteors = arcade.SpriteList()


def setup():
    global background_img, player

    player = Ship(filename="../assets/space_shooter/PNG/playerShip1_red.png",
                  center_x=WIDTH/2, center_y=HEIGHT/2,
                  scale=0.5)

    # create powerups
    # for _ in range(10):
    #     powerup = PowerUp("../assets/space_shooter/PNG/Power-ups/powerupGreen_star.png", 0.5)
    #     powerup.position = Vec2d(random.randrange(WIDTH), random.randrange(HEIGHT))
    #     powerup.velocity = Vec2d(random.randrange(-2, 2), random.randrange(-2, 2))
    #     powerups.append(powerup)

    # for meteor in asdict(levels[0]).get("meteors"):
    #     meteors.append(meteor)


    arcade.open_window(WIDTH, HEIGHT, "Spacer")
    arcade.set_background_color(arcade.color.BLACK)
    arcade.schedule(on_update, 1/80)

    window = arcade.get_window()
    window.on_draw = on_draw
    window.on_key_press = on_key_press
    window.on_key_release = on_key_release
    window.on_mouse_press = on_mouse_press

    arcade.run()


def on_update(delta_time):
    global score

    # player actions
    if keys_pressed[arcade.key.SPACE]:
        lazer = player.fire_lazer()
        if lazer:
            player_lazerbolts.append(lazer)

    # movement
    if keys_pressed[arcade.key.W]:
        player.thrust_longitudinal(Ship.Thrust.FORWARD)
    if keys_pressed[arcade.key.S]:
        player.thrust_longitudinal(Ship.Thrust.BACKWARD)
    if keys_pressed[arcade.key.A]:
        player.thrust_rotational(Ship.Thrust.CCW)
    if keys_pressed[arcade.key.D]:
        player.thrust_rotational(Ship.Thrust.CW)

    player.update()
    powerups.update()
    player_lazerbolts.update()
    meteors.update()

    # lazer bolt distance checks
    for lazer in player_lazerbolts:
        center = Vec2d(WIDTH / 2, HEIGHT / 2)
        max_dist = center.get_distance(Vec2d.zero())
        if lazer.position.get_distance(center) > max_dist:
            lazer.kill()

    powerup_collisions = arcade.check_for_collision_with_list(player, powerups)
    if powerup_collisions:
        for powerup in powerup_collisions:
            powerup.kill()
            score += 1

    # powerup boundary checks
    for pu in powerups:
        if pu.position.x < 0:
            pu.position.x = 0
            pu.velocity.x *= -1
        elif pu.position.x > WIDTH:
            pu.position.x = WIDTH
            pu.velocity.x *= -1

        if pu.position.y < 0:
            pu.position.y = 0
            pu.velocity.y *= -1
        elif pu.position.y > HEIGHT:
            pu.position.y = HEIGHT
            pu.velocity.y *= -1


def on_draw():
    arcade.start_render()

    # draw background tiled
    arcade.draw_texture_rectangle(WIDTH/2, HEIGHT/2,
                                  WIDTH, HEIGHT,
                                  background_img,
                                  repeat_count_x=WIDTH//background_img.width,
                                  repeat_count_y=HEIGHT//background_img.height)

    powerups.draw()
    player_lazerbolts.draw()
    player.draw()
    meteors.draw()
    powerups.draw()

    arcade.draw_text(f"Score: {score}", 50, 50, arcade.color.WHITE, 34)

    # draw location assist
    if player.position.x < 0 or player.position.x > WIDTH or player.position.y < 0 or player.position.y > HEIGHT:
        radius = player.texture.width/2
        x = max(min(WIDTH-radius, player.position.x), radius)
        y = max(min(HEIGHT-radius, player.position.y), radius)

        arcade.draw_circle_filled(x, y, radius, color=(*arcade.color.WHITE, 255//4))
        arcade.draw_texture_rectangle(x, y, player.texture.width*0.7, player.texture.height*0.7,
                                      player.texture, alpha=1, angle=player.angle)


def on_key_press(key, modifiers):
    keys_pressed[key] = True


def on_key_release(key, modifiers):
    keys_pressed[key] = False


def on_mouse_press(x, y, button, modifiers):
    global meteors
    click_sprite = arcade.Sprite(center_x=x, center_y=y)
    click_sprite.width = 1
    click_sprite.height = 1

    if button == 1:  # left mouse
        collisions = arcade.check_for_collision_with_list(click_sprite, meteors)

        if collisions:
            for meteor in collisions:
                meteor.kill()
        else:
            meteor = Meteor(x, y, size=Meteor.Size.BIG1)
            meteors.append(meteor)
    elif button == 4:  # right mouse
        collisions = arcade.check_for_collision_with_list(click_sprite, powerups)

        if collisions:
            for powerup in collisions:
                powerup.kill()
        else:
            powerup = PowerUp(filename="../assets/space_shooter/PNG/Power-ups/powerupGreen_star.png",
                              center_x=x,
                              center_y=y,
                              scale=0.5)
            powerups.append(powerup)


if __name__ == '__main__':
    setup()
