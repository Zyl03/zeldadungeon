import pygame
import json
import asyncio
import os
from bfs import breadth_first_search

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

stats_lines = [
     f"Path Length: {70}",
     f"Visited: {80}",
     f"Frontier: {90}"
]

def find_start(g):
    for r in range(len(g)):
        for c in range(len(g[0])):
            if g[r][c] == 'S':
                return (r, c)
    return (0, 0)

def draw_grid(screen, g, ox, oy):
    for r in range(ROWS):
        for c in range(COLS):
            cell = g[r][c]
            x = c * TILE_SIZE + ox
            y = r * TILE_SIZE + oy
            if cell == "#":
                screen.blit(wall_img, (x, y))
            elif cell == ".":
                screen.blit(road_img, (x, y))
            elif cell == "F":
                screen.blit(food_img, (x, y))
            elif cell == "M":
                screen.blit(monster_img, (x, y))
            elif cell == "~":
                screen.blit(water_img, (x, y))
            elif cell == "S":
                screen.blit(start_img, (x, y))
            elif cell == "E":
                screen.blit(end_img, (x, y))
            
def draw_player(screen, pos, ox, oy):
    row, col = pos
    x,y = col * TILE_SIZE + ox,row * TILE_SIZE + oy
    halo_radius = TILE_SIZE // 2
    cx, cy = x + TILE_SIZE//2, y + TILE_SIZE//2
    pygame.draw.circle(screen, (255, 216, 77), (cx, cy), halo_radius) 
    screen.blit(player_img, (x, y))

def draw_overlay_cells(screen, cells, color, tile_size, offset_x=0, offset_y=0, alpha=90):
    overlay = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
    overlay.fill((*color, alpha))
    for r, c in cells:
        x = c * tile_size + offset_x
        y = r * tile_size + offset_y
        screen.blit(overlay, (x, y))

def draw_centered_lines(screen, lines, font, color, center_x, start_y, line_gap):
    for i, line in enumerate(lines):
        surf = font.render(line, True, color)
        rect = surf.get_rect(center=(center_x, start_y + i * line_gap))
        screen.blit(surf, rect)

async def main():
    clock = pygame.time.Clock()

    player_pos = find_start(grid)

    snapshots = []
    frame_index = 0
    animating = False
    last_frame_time = 0
    frame_delay = 300
    show_solution = False

    with open("data/path.json", "r") as file:
        path = json.load(file)

    with open("data/frontier.json", "r") as frontier_file:
        frontier = json.load(frontier_file)

    with open("data/expanded.json", "r") as expanded_file:
        expanded = json.load(expanded_file)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                row, col = player_pos
                if event.key == pygame.K_DOWN:
                    player_pos = (row + 1, col)
                if event.key == pygame.K_UP:
                    player_pos = (row - 1, col)
                if event.key == pygame.K_LEFT:
                    player_pos = (row, col - 1)
                if event.key == pygame.K_RIGHT:
                    player_pos = (row, col + 1)
                if event.key == pygame.K_SPACE:
                     steps, queue_max, expanded_count, queue_snap,snapshots = breadth_first_search(player_pos[0], player_pos[1], 0)
                     frame_index = 0
                     animating = len(snapshots) > 0
                     last_frame_time = pygame.time.get_ticks()
                if event.key == pygame.K_p:
                    show_solution = not show_solution
    
        if animating and len(snapshots) > 0 and frame_index < len(snapshots) - 1:
            now = pygame.time.get_ticks()
            if now - last_frame_time > frame_delay:
                frame_index += 1
                last_frame_time = now

        screen.fill((30, 30, 30))
        draw_grid(screen, grid, 0, 0)
        draw_player(screen, player_pos, 0, 0)

        if show_solution:
            draw_overlay_cells(screen, path, (0,255,120), TILE_SIZE, alpha=120)

        if animating and len(snapshots) > 0:
                frame = snapshots[frame_index]
                visited = frame["visited"]
                current_frontier = frame["frontier"]
                current = frame["current"]

                draw_overlay_cells(screen, visited, (255, 80, 80), TILE_SIZE, alpha=70)
                draw_overlay_cells(screen, current_frontier, (80, 170, 255), TILE_SIZE, alpha=180)
                draw_overlay_cells(screen, [current], (255, 255, 0), TILE_SIZE, alpha=230)

        pygame.draw.rect(screen, (25, 25, 25), (ui_x, 0, UI_WIDTH, HEIGHT))
        pygame.draw.line(screen, (80, 80, 80), (ui_x, 0), (ui_x, HEIGHT), 2)

        screen.blit(panel_bg, (WIDTH, 0))

        panel_center_x = WIDTH + UI_WIDTH // 2
        draw_centered_lines(screen, legend_lines, legend_font, TEXT_COLOR, panel_center_x, 200, 25)
        draw_centered_lines(screen, controls_lines, legend_font, TEXT_COLOR, panel_center_x, 400, 25)
        draw_centered_lines(screen, stats_lines, stats_font, TEXT_COLOR, panel_center_x, 600, 25)

        pygame.display.flip()
        clock.tick(60)

        await asyncio.sleep(0)

    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())