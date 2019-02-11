import arcade


WIDTH = 640
HEIGHT = 480

GRID_COLS = 10
GRID_ROWS = 10

CELL_WIDTH = WIDTH // GRID_COLS
CELL_HEIGHT = HEIGHT // GRID_ROWS

arcade.open_window(WIDTH, HEIGHT, "Drawing Grid Lines")
arcade.set_background_color(arcade.color.WHITE)
arcade.start_render()
# >>> draw here

# vertical lines
for x in range(0, WIDTH, CELL_WIDTH):
    arcade.draw_line(x, 0, x, HEIGHT, arcade.color.BLACK, border_width=2)

# horizontal lines
for y in range(0, HEIGHT, CELL_HEIGHT):
    arcade.draw_line(0, y, WIDTH, y, arcade.color.GRAY, border_width=2)

# <<< end draw
arcade.finish_render()
arcade.run()
