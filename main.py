import pygame
import json
import asyncio
import os
from bfs import breadth_first_search
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

def dash_board():
     pygame.draw.rect(screen, (25, 25, 25), (ui_x, 0, UI_WIDTH, HEIGHT))
     pygame.draw.line(screen, (80, 80, 80), (ui_x, 0), (ui_x, HEIGHT), 2)
     screen.blit(panel_bg, (WIDTH, 0))
     panel_center_x = WIDTH + UI_WIDTH // 2
     draw_centered_lines(screen, legend_lines, legend_font, TEXT_COLOR, panel_center_x, 200, 25)
     draw_centered_lines(screen, controls_lines, legend_font, TEXT_COLOR, panel_center_x, 400, 25)

async def main():
    clock = pygame.time.Clock()

    player_pos = find_start(grid)
    player_hp = 100
    food_count = 0
    moves_made = 0

    game_over = False
    win = False

    snapshots = []
    frame_index = 0
    path_frame = 0
    last_frame_time = 0
    frame_delay = 100

    animating = False
    animating_path = False
    show_solution = False
    running = True

    panel_center_x = WIDTH + UI_WIDTH // 2
    
    stats_lines = [
                        f"Path Length: {0}",
                        f"Visited: {0}",
                        f"HP: {player_hp}",
                        f"Food: {food_count}",
                    ]
    
    with open("data/path.json", "r") as file:
        path = json.load(file)

    while running:
        
        # --------------------
        # 1. handle events
        # --------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if game_over:
                    continue
                r, c = player_pos
                nr, nc = r, c
                if event.key == pygame.K_DOWN:
                    nr += 1
                if event.key == pygame.K_UP:
                    nr -= 1
                if event.key == pygame.K_LEFT:
                    nc -= 1
                if event.key == pygame.K_RIGHT:
                    nc += 1

                if (nr, nc) != (r, c):
                    if 0 <= nr < ROWS and 0 <= nc < COLS:
                        if grid[nr][nc] != "#":
                            player_pos = (nr, nc)
                            moves_made += 1
                    steps, expanded_count, _ = breadth_first_search(
                        player_pos[0],
                        player_pos[1],
                        0
                    )

                r, c = player_pos
                if grid[r][c] == "F":
                    player_hp = min(100, player_hp + 20)
                    food_count += 1
                    grid[r][c] = "."

                if grid[r][c] == "M":
                    player_hp -= 25

                if grid[r][c] == "E":
                    win = True
                    game_over = True
                
                if grid[r][c] == "~":
                    player_hp -= 5

                if player_hp <= 0:
                    game_over = True

                if event.key == pygame.K_SPACE:
                    steps,  expanded_count, snapshots = breadth_first_search(
                        player_pos[0], player_pos[1], 0
                    )
                    frame_index = 0
                    path_frame = 0
                    animating = len(snapshots) > 0
                    animating_path = False
                    last_frame_time = pygame.time.get_ticks()

                if event.key == pygame.K_p:
                    show_solution = not show_solution

                if event.key == pygame.K_r:
                    grid[:] = copy.deepcopy(original_grid)

                    player_pos = find_start(grid)

                    player_hp = 100
                    food_count = 0
                    moves_made = 0

                    steps = 0
                    expanded_count = 0

                    game_over = False
                    win = False

                    snapshots = []
                    frame_index = 0
                    path_frame = 0

                    animating = False
                    animating_path = False
                    show_solution = False

                    stats_lines = [
                        f"Path Length: {0}",
                        f"Visited: {0}",
                        f"HP: {player_hp}",
                        f"Heart: {food_count}",
                    ]

        now = pygame.time.get_ticks()

        # Stage 1: expanded/frontier animation
        if animating and len(snapshots) > 0:
            if now - last_frame_time > frame_delay:
                if frame_index < len(snapshots) - 1:
                    frame_index += 1
                    last_frame_time = now
                else:
                    animating = False
                    animating_path = True
                    path_frame = 0
                    last_frame_time = now

        # Stage 2: backtracking animation
        elif animating_path:
            if now - last_frame_time > 120:
                if path_frame < len(path):
                    path_frame += 1
                    last_frame_time = now
                else:
                    animating_path = False

        # --------------------
        # 3. draw
        # --------------------
        screen.fill((30, 30, 30))
        draw_grid(screen, grid, 0, 0)
        draw_player(screen, player_pos, 0, 0)

        # Show full solution if toggled
        if show_solution:
            draw_overlay_cells(screen, path, (0, 255, 120), TILE_SIZE, alpha=120)

        # Draw BFS snapshots
        if len(snapshots) > 0 and frame_index < len(snapshots):
            frame = snapshots[frame_index]
            visited = frame["visited"]
            current_frontier = frame["frontier"]
            current = frame["current"]

            draw_overlay_cells(screen, visited, (255, 80, 80), TILE_SIZE, alpha=70)
            draw_overlay_cells(screen, current_frontier, (80, 170, 255), TILE_SIZE, alpha=180)
            draw_overlay_cells(screen, [current], (255, 255, 0), TILE_SIZE, alpha=230)
    
        # Draw path step by step
        if animating_path or path_frame > 0:
            draw_overlay_cells(screen, path[:path_frame], (0, 255, 120), TILE_SIZE, alpha=180)
        
        stats_lines = [
            f"Moves: {moves_made}",
            f"Path Length: {steps if 'steps' in locals() else 0}",
            f"HP: {player_hp}",
            f"Heart: {food_count}",
        ]

        dash_board()
        draw_centered_lines(screen, stats_lines, stats_font, TEXT_COLOR, panel_center_x, 600, 25)
        if win:
                    font = pygame.font.SysFont(None, 80)
                    text = font.render("YOU WIN!", True, (0, 255, 0))
                    screen.blit(text, (WIDTH//2 - 150, HEIGHT//2))

        if game_over and not win:
                    font = pygame.font.SysFont(None, 80)
                    text = font.render("GAME OVER", True, (255, 0, 0))
                    screen.blit(text, (WIDTH//2 - 180, HEIGHT//2))
        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)

    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())