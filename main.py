import pygame
import json
import asyncio
import os

from bfs import *
from render import *
from assets import *

import copy

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
        draw_grid(
        screen, grid, 0, 0,
        ROWS, COLS, TILE_SIZE,
        wall_img, road_img, food_img,
        monster_img, water_img,
        start_img, end_img
        )
        draw_player(screen, player_pos, 0, 0, TILE_SIZE, player_img)

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

        dash_board(screen, ui_x, UI_WIDTH, HEIGHT, WIDTH,
               panel_bg, legend_lines, controls_lines,
               legend_font, TEXT_COLOR)
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