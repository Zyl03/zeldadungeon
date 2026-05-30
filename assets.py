import pygame
import os
import copy

grid = [
list("#########################"),
list("#S..#..F..#...#M....#...#"),
list("###.#.###.#.#.#.###.#.#.#"),
list("#...#...#...#...#...#.#.#"),
list("#.#####.#####.###.###.#.#"),
list("#..~..#.....#...#.....#.#"),
list("#.###.#####.###.#####.#.#"),
list("#.#...#..F#...M.....#...#"),
list("#.#.###.#.###.#.###.###.#"),
list("#.#.....#.....#.#.~.#...#"),
list("#.###########.#.#.###.#.#"),
list("#.....#.....#.#.#...#.#.#"),
list("###.#.#.###.#.#.###.#.#.#"),
list("#...#...#...#.#...#...#.#"),
list("#.#####.#.###.###.#####.#"),
list("#..M..#.#...#...#..F..#.#"),
list("#.###.#.###.###.#####.#.#"),
list("#.#...#...#.~...#...#...#"),
list("#.#.#####.#######.#.###.#"),
list("#.#..~..#.....#...#...#.#"),
list("#.#####.#####.#.#####.#M#"),
list("#..F..#.....#.#.....#.#.#"),
list("#.###.#####.#.###.#.#.#.#"),
list("#...#.....#.....#...#..E#"),
list("#########################"),
]

original_grid = copy.deepcopy(grid)
ROWS = len(grid)
COLS = len(grid[0])

TILE_SIZE = 32
GRID_W = COLS * TILE_SIZE
GRID_H = ROWS * TILE_SIZE

WIDTH = GRID_W
UI_WIDTH = 260
HEIGHT = GRID_H
ui_x = WIDTH
TEXT_COLOR = (235, 215, 160)

pygame.init()

screen = pygame.display.set_mode((WIDTH + UI_WIDTH, HEIGHT))
pygame.display.set_caption("Zelda Dungeon")

font_path = os.path.join("fonts", "Cinzel-Regular.ttf")
legend_font = pygame.font.Font(font_path, 20)
stats_font = pygame.font.Font(font_path, 20)

wall_img = pygame.image.load("image/wall.png").convert_alpha()
player_img = pygame.image.load("image/player.png").convert_alpha()
road_img = pygame.image.load("image/road.png").convert_alpha()
food_img = pygame.image.load("image/food.png").convert_alpha()
monster_img = pygame.image.load("image/monster.png").convert_alpha()
water_img = pygame.image.load("image/water.png").convert_alpha()
start_img = pygame.image.load("image/start.png").convert_alpha()
end_img = pygame.image.load("image/end.png").convert_alpha()

wall_img = pygame.transform.scale(wall_img, (TILE_SIZE, TILE_SIZE))
player_img = pygame.transform.scale(player_img, (TILE_SIZE, TILE_SIZE))
road_img = pygame.transform.scale(road_img, (TILE_SIZE, TILE_SIZE))
food_img = pygame.transform.scale(food_img, (TILE_SIZE, TILE_SIZE))
monster_img = pygame.transform.scale(monster_img, (TILE_SIZE, TILE_SIZE))
water_img =  pygame.transform.scale(water_img, (TILE_SIZE, TILE_SIZE))
start_img =  pygame.transform.scale(start_img, (TILE_SIZE, TILE_SIZE))
end_img =  pygame.transform.scale(end_img, (TILE_SIZE, TILE_SIZE))

panel_path = os.path.join("image", "background.png")
panel_bg = pygame.image.load(panel_path).convert_alpha()
panel_bg = pygame.transform.smoothscale(panel_bg, (UI_WIDTH, HEIGHT))

tile_img = {
    '#': wall_img,
    '.': road_img,
    'S': start_img,
    'E': end_img,
    '~': water_img,
    'M': monster_img,
    'F': food_img,
}

legend_lines = [
    "S = Start",
    "E = Exit",
    "Red = Visited",
    "Green = Path",
    "Blue = Frontier"
]

controls_lines = [
    "Arrows = Move",
    "Space = Animation",
    "P = Toggle Path",
    "R = Reset"
]