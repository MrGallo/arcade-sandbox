"""
Draws a player on a grid based on a position from 0-99 in a Snakes and Ladders type game.
Mouse-wheel up/down to move the player.
"""

import arcade


WIDTH = 640
HEIGHT = 480

GRID_COLS = 10
GRID_ROWS = 10

CELL_WIDTH = WIDTH // GRID_COLS
CELL_HEIGHT = HEIGHT // GRID_ROWS

#: int: The player's position from 0-99 on a snakes and ladder board.
player_position = 0


def setup():
    arcade.open_window(WIDTH, HEIGHT, "Drawing Grid Lines")
    arcade.set_background_color(arcade.color.WHITE)
    arcade.schedule(update, 1/60)

    # Override arcade window methods
    window = arcade.get_window()
    window.on_draw = on_draw
    window.on_mouse_scroll = on_mouse_scroll

    arcade.run()


def update(delta_time):
    pass


def on_draw():
    arcade.start_render()

    # vertical lines
    for x in range(0, WIDTH, CELL_WIDTH):
        arcade.draw_line(x, 0, x, HEIGHT, arcade.color.BLACK, border_width=2)

    # horizontal lines
    for y in range(0, HEIGHT, CELL_HEIGHT):
        arcade.draw_line(0, y, WIDTH, y, arcade.color.GRAY, border_width=2)

    # Draw player on board
    #   convert player_position to 2D grid positions
    player_row = player_position // GRID_ROWS

    if player_row % 2 == 0:
        player_col = player_position % GRID_COLS
    else:
        player_col = (GRID_COLS - 1) - (player_position % GRID_COLS)

    #   Translate grid position to pixels (center point)
    player_center_x = player_col*CELL_WIDTH + CELL_WIDTH/2
    player_center_y = player_row*CELL_HEIGHT + CELL_HEIGHT/2

    #   Draw the player at the calculated coordinates
    radius = min(CELL_WIDTH, CELL_HEIGHT) / 2
    arcade.draw_circle_filled(player_center_x, player_center_y, radius, arcade.color.BLUE)


def on_mouse_scroll(x, y, scroll_x, scroll_y):
    global player_position
    player_position += scroll_y
    player_position = max(0, player_position)   # prevent positions below 0
    player_position = min(99, player_position)  # prevent positions above 99


if __name__ == '__main__':
    setup()
