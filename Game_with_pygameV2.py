import pygame
import random
import sys
import math

pygame.init()

# -----------------------
# CONFIG
# -----------------------
WIDTH, HEIGHT = 720, 860
TOP_BAR_HEIGHT = 120
BOTTOM_BAR_HEIGHT = 120
BOARD_SIZE = 660
BOARD_X = (WIDTH - BOARD_SIZE) // 2
BOARD_Y = TOP_BAR_HEIGHT
CELL_SIZE = BOARD_SIZE // 3

FPS = 60

WHITE = (255, 255, 255)
SOFT_WHITE = (220, 230, 255)
BLACK = (5, 8, 20)
DARK_BLUE = (10, 15, 40)
MID_BLUE = (20, 30, 70)
CYAN = (150, 220, 255)
RED = (255, 120, 140)
BLUE = (120, 200, 255)
GRAY = (140, 150, 180)
GLOW = (180, 220, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Tic-Tac-Toe")
clock = pygame.time.Clock()

TITLE_FONT = pygame.font.SysFont("arial", 44, bold=True)
TURN_FONT = pygame.font.SysFont("arial", 34, bold=True)
SYMBOL_FONT = pygame.font.SysFont("arial", 110, bold=True)
CELL_NUM_FONT = pygame.font.SysFont("arial", 34, bold=True)
MSG_FONT = pygame.font.SysFont("arial", 36, bold=True)
BTN_FONT = pygame.font.SysFont("arial", 28, bold=True)


# -----------------------
# YOUR GAME LOGIC
# -----------------------
def choose_beginner() -> str:
    x = random.randint(0, 1)
    if x == 0:
        return 'x'
    return 'o'


def create_board() -> list:
    board = list(range(1, 9 + 1))
    return board


def make_move(board, position, symbol):
    if symbol == 'x':
        board.insert(position - 1, 'x')
        board.remove(position)
    else:
        board.insert(position - 1, 'o')
        board.remove(position)


def check_winner(board, symbol):
    winning_combinations = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6]
    ]
    for i in winning_combinations:
        if board[i[0]] == board[i[1]] == board[i[2]] == symbol:
            return True
    return False


def is_tie(board) -> bool:
    if any(isinstance(i, int) for i in board):
        return False
    return True


def switch_player(current):
    if current == 'o':
        return 'x'
    return 'o'


def player_winning_count(player, winning_count) -> list:
    if player == 'x':
        winning_count[0] += 1
        return winning_count
    winning_count[1] += 1
    return winning_count


# -----------------------
# UI HELPERS
# -----------------------
def draw_vertical_gradient(surface, top_color, bottom_color):
    for y in range(surface.get_height()):
        ratio = y / surface.get_height()
        r = int(top_color[0] + (bottom_color[0] - top_color[0]) * ratio)
        g = int(top_color[1] + (bottom_color[1] - top_color[1]) * ratio)
        b = int(top_color[2] + (bottom_color[2] - top_color[2]) * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y), (surface.get_width(), y))


def create_star_field(count=90):
    stars = []
    for _ in range(count):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        radius = random.randint(1, 3)
        alpha = random.randint(100, 255)
        speed = random.uniform(0.2, 1.0)
        phase = random.uniform(0, math.pi * 2)
        stars.append({
            "x": x,
            "y": y,
            "r": radius,
            "a": alpha,
            "speed": speed,
            "phase": phase
        })
    return stars


stars = create_star_field()


def draw_stars(surface, tick):
    for star in stars:
        pulse = (math.sin(tick * 0.02 * star["speed"] + star["phase"]) + 1) / 2
        alpha = int(100 + 155 * pulse)
        glow_r = star["r"] + 2

        glow_surf = pygame.Surface((glow_r * 6, glow_r * 6), pygame.SRCALPHA)
        pygame.draw.circle(
            glow_surf,
            (255, 255, 255, alpha // 6),
            (glow_surf.get_width() // 2, glow_surf.get_height() // 2),
            glow_r * 2
        )
        surface.blit(glow_surf, (star["x"] - glow_surf.get_width() // 2, star["y"] - glow_surf.get_height() // 2))

        dot_surf = pygame.Surface((star["r"] * 4, star["r"] * 4), pygame.SRCALPHA)
        pygame.draw.circle(
            dot_surf,
            (255, 255, 255, alpha),
            (dot_surf.get_width() // 2, dot_surf.get_height() // 2),
            star["r"]
        )
        surface.blit(dot_surf, (star["x"] - dot_surf.get_width() // 2, star["y"] - dot_surf.get_height() // 2))


def draw_glow_line(surface, color, start_pos, end_pos, width=2, glow_layers=4):
    for i in range(glow_layers, 0, -1):
        glow_width = width + i * 4
        alpha = max(20, 80 - i * 12)
        temp = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.line(temp, (*color, alpha), start_pos, end_pos, glow_width)
        surface.blit(temp, (0, 0))
    pygame.draw.line(surface, color, start_pos, end_pos, width)


def draw_glow_rect(surface, rect, color, radius=18, glow=18, alpha=70):
    for i in range(glow, 0, -4):
        temp = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(
            temp,
            (*color, max(10, alpha - i * 2)),
            rect.inflate(i * 2, i * 2),
            border_radius=radius + i
        )
        surface.blit(temp, (0, 0))


def get_cell_rect(index):
    row = index // 3
    col = index % 3
    return pygame.Rect(
        BOARD_X + col * CELL_SIZE,
        BOARD_Y + row * CELL_SIZE,
        CELL_SIZE,
        CELL_SIZE
    )


def get_position_from_mouse(pos, board):
    mx, my = pos
    if not (BOARD_X <= mx < BOARD_X + BOARD_SIZE and BOARD_Y <= my < BOARD_Y + BOARD_SIZE):
        return None

    col = (mx - BOARD_X) // CELL_SIZE
    row = (my - BOARD_Y) // CELL_SIZE
    position = row * 3 + col + 1

    if position in board:
        return position
    return None


def draw_x(surface, rect, scale=1.0):
    cx, cy = rect.center
    size = int(40 * scale)
    line_w = max(6, int(8 * scale))

    # glow
    temp = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.line(temp, (*RED, 50), (cx - size, cy - size), (cx + size, cy + size), line_w + 12)
    pygame.draw.line(temp, (*RED, 50), (cx + size, cy - size), (cx - size, cy + size), line_w + 12)
    surface.blit(temp, (0, 0))

    pygame.draw.line(surface, RED, (cx - size, cy - size), (cx + size, cy + size), line_w)
    pygame.draw.line(surface, RED, (cx + size, cy - size), (cx - size, cy + size), line_w)


def draw_o(surface, rect, scale=1.0):
    cx, cy = rect.center
    radius = int(42 * scale)
    line_w = max(6, int(8 * scale))

    temp = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.circle(temp, (*BLUE, 50), (cx, cy), radius + 8, line_w + 8)
    surface.blit(temp, (0, 0))

    pygame.draw.circle(surface, BLUE, (cx, cy), radius, line_w)


def draw_board(board, player, scores, hover_index, tick, message=""):
    draw_vertical_gradient(screen, BLACK, DARK_BLUE)
    draw_stars(screen, tick)

    # Top title
    title = TITLE_FONT.render("TIC TAC TOE", True, WHITE)
    title_rect = title.get_rect(center=(WIDTH // 2, 34))
    screen.blit(title, title_rect)

    turn_text = TURN_FONT.render(f"PLAYER {player.upper()} TURN", True, SOFT_WHITE)
    turn_rect = turn_text.get_rect(center=(WIDTH // 2, 82))
    screen.blit(turn_text, turn_rect)

    # Board glow frame
    board_rect = pygame.Rect(BOARD_X, BOARD_Y, BOARD_SIZE, BOARD_SIZE)
    draw_glow_rect(screen, board_rect, GLOW, radius=28, glow=16, alpha=38)

    # Hover animation
    if hover_index is not None and isinstance(board[hover_index], int):
        cell_rect = get_cell_rect(hover_index)
        pulse = 0.5 + 0.5 * math.sin(tick * 0.12)
        inflate = int(6 + pulse * 8)
        hover_rect = cell_rect.inflate(-18 + inflate, -18 + inflate)

        temp = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(temp, (255, 255, 255, 18), hover_rect, border_radius=18)
        pygame.draw.rect(temp, (180, 220, 255, 70), hover_rect, width=2, border_radius=18)
        screen.blit(temp, (0, 0))

    # Grid lines with glow
    for i in range(1, 3):
        x = BOARD_X + i * CELL_SIZE
        y = BOARD_Y + i * CELL_SIZE

        draw_glow_line(screen, WHITE, (x, BOARD_Y), (x, BOARD_Y + BOARD_SIZE), width=3, glow_layers=5)
        draw_glow_line(screen, WHITE, (BOARD_X, y), (BOARD_X + BOARD_SIZE, y), width=3, glow_layers=5)

    # Symbols / numbers
    for i in range(9):
        rect = get_cell_rect(i)
        center_rect = rect.inflate(-28, -28)

        value = board[i]

        if value == 'x':
            draw_x(screen, center_rect, 1.0)
        elif value == 'o':
            draw_o(screen, center_rect, 1.0)
        else:
            num_text = CELL_NUM_FONT.render(str(value), True, (190, 205, 240))
            num_rect = num_text.get_rect(center=rect.center)
            screen.blit(num_text, num_rect)

            if hover_index == i:
                ghost_scale = 0.85 + 0.1 * math.sin(tick * 0.12)
                if player == 'x':
                    draw_x(screen, center_rect, ghost_scale)
                else:
                    draw_o(screen, center_rect, ghost_scale)

    # Bottom score / message panel
    bottom_rect = pygame.Rect(40, HEIGHT - 95, WIDTH - 80, 60)
    draw_glow_rect(screen, bottom_rect, GLOW, radius=18, glow=12, alpha=24)

    score_text = BTN_FONT.render(
        f"X: {scores[0]}        O: {scores[1]}",
        True,
        WHITE
    )
    score_rect = score_text.get_rect(midleft=(70, HEIGHT - 65))
    screen.blit(score_text, score_rect)

    if message:
        msg = BTN_FONT.render(message, True, CYAN)
        msg_rect = msg.get_rect(midright=(WIDTH - 70, HEIGHT - 65))
        screen.blit(msg, msg_rect)

    pygame.display.update()


def draw_end_buttons():
    yes_rect = pygame.Rect(WIDTH // 2 - 170, HEIGHT - 170, 150, 56)
    no_rect = pygame.Rect(WIDTH // 2 + 20, HEIGHT - 170, 150, 56)

    mouse_pos = pygame.mouse.get_pos()

    for rect, text, base_color in [
        (yes_rect, "PLAY AGAIN", (80, 170, 255)),
        (no_rect, "QUIT", (255, 100, 120))
    ]:
        hovered = rect.collidepoint(mouse_pos)
        glow_color = (200, 230, 255) if hovered else base_color
        draw_glow_rect(screen, rect, glow_color, radius=16, glow=12 if hovered else 8, alpha=35)
        pygame.draw.rect(screen, (*glow_color,), rect, border_radius=16, width=2)

        label = BTN_FONT.render(text, True, WHITE)
        label_rect = label.get_rect(center=rect.center)
        screen.blit(label, label_rect)

    pygame.display.update()
    return yes_rect, no_rect


def wait_for_play_again(board, player, scores, tick, message):
    while True:
        draw_board(board, player, scores, None, tick, message)
        yes_rect, no_rect = draw_end_buttons()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if yes_rect.collidepoint(event.pos):
                    return True
                if no_rect.collidepoint(event.pos):
                    return False

        tick += 1
        clock.tick(FPS)


# -----------------------
# GAME LOOP
# -----------------------
def play_game():
    board = create_board()
    player = choose_beginner()
    winning_count = [0, 0]
    tick = 0

    while True:
        board = create_board()
        message = ""
        round_over = False

        while True:
            hover_index = None
            mouse_pos = pygame.mouse.get_pos()

            for i in range(9):
                if get_cell_rect(i).collidepoint(mouse_pos):
                    hover_index = i
                    break

            draw_board(board, player, winning_count, hover_index, tick, message)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and not round_over:
                    position = get_position_from_mouse(event.pos, board)

                    if position is not None:
                        make_move(board, position, player)

                        if check_winner(board, player):
                            message = f"PLAYER {player.upper()} WINS"
                            winning_count = player_winning_count(player, winning_count)
                            draw_board(board, player, winning_count, None, tick, message)
                            round_over = True
                            break

                        if is_tie(board):
                            message = "IT'S A TIE"
                            draw_board(board, player, winning_count, None, tick, message)
                            player = switch_player(player)
                            round_over = True
                            break

                        player = switch_player(player)

            if round_over:
                pygame.time.delay(700)
                if not wait_for_play_again(board, player, winning_count, tick, message):
                    pygame.quit()
                    sys.exit()
                break

            tick += 1
            clock.tick(FPS)


play_game()