import pygame

def find_start(g):
    for r in range(len(g)):
        for c in range(len(g[0])):
            if g[r][c] == 'S':
                return (r, c)
    return (0, 0)

def draw_grid(screen, g, ox, oy, ROWS, COLS, TILE_SIZE,
              wall_img, road_img, food_img, monster_img,
              water_img, start_img, end_img):

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


def draw_player(screen, pos, ox, oy, TILE_SIZE, player_img):
    row, col = pos
    x = col * TILE_SIZE + ox
    y = row * TILE_SIZE + oy

    halo_radius = TILE_SIZE // 2
    cx, cy = x + TILE_SIZE // 2, y + TILE_SIZE // 2

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


def dash_board(screen, ui_x, UI_WIDTH, HEIGHT, WIDTH,
               panel_bg, legend_lines, controls_lines,
               legend_font, TEXT_COLOR):

    pygame.draw.rect(screen, (25, 25, 25), (ui_x, 0, UI_WIDTH, HEIGHT))
    pygame.draw.line(screen, (80, 80, 80), (ui_x, 0), (ui_x, HEIGHT), 2)

    screen.blit(panel_bg, (WIDTH, 0))

    panel_center_x = WIDTH + UI_WIDTH // 2

    draw_centered_lines(screen, legend_lines, legend_font, TEXT_COLOR,
                        panel_center_x, 200, 25)

    draw_centered_lines(screen, controls_lines, legend_font, TEXT_COLOR,
                        panel_center_x, 400, 25)