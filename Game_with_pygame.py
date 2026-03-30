import pygame
import random
import sys

pygame.init()

# -----------------------
# CONFIG
# -----------------------
WIDTH, HEIGHT = 600, 750
BOARD_SIZE = 600
ROWS, COLS = 3, 3
CELL_SIZE = BOARD_SIZE // 3

LINE_WIDTH = 6
FONT = pygame.font.SysFont(None, 60)
SMALL_FONT = pygame.font.SysFont(None, 36)
BIG_FONT = pygame.font.SysFont(None, 50)

WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GRAY = (180, 180, 180)
BLUE = (50, 90, 200)
RED = (200, 50, 50)
GREEN = (50, 150, 70)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")


# -----------------------
# YOUR LOGIC
# -----------------------
def choose_beginner() -> str:
    # the func will return who is begins the game
    x = random.randint(0, 1)
    if x == 0:
        return 'x'
    return 'o'


def create_board() -> list:
    # the func will return a new empty board
    board = list(range(1, 9 + 1))
    return board


def make_move(board, position, symbol):
    # the func will update the board with the user's choice
    if symbol == 'x':
        board.insert(position - 1, 'x')
        board.remove(position)
    else:
        board.insert(position - 1, 'o')
        board.remove(position)


def check_winner(board, symbol):
    # checks if there is a winner, and who is it
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
    # the func check if there's a tie
    if any(isinstance(i, int) for i in board):  # isinstance checks if a value is a specific type
        return False
    return True


def switch_player(current):
    # the func will switch turns
    if current == 'o':
        return 'x'
    return 'o'


def player_winning_count(player, winning_count) -> list:
    # the function updates the scores of the players
    if player == 'x':
        winning_count[0] += 1
        return winning_count
    winning_count[1] += 1
    return winning_count


# -----------------------
# PYGAME HELPERS
# -----------------------
def draw_board(board, player, winning_count, message=""):
    screen.fill(WHITE)

    # grid
    for i in range(1, 3):
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (BOARD_SIZE, i * CELL_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, BOARD_SIZE), LINE_WIDTH)

    # cells
    for i in range(9):
        row = i // 3
        col = i % 3
        x = col * CELL_SIZE
        y = row * CELL_SIZE

        value = board[i]
        center_x = x + CELL_SIZE // 2
        center_y = y + CELL_SIZE // 2

        if value == 'x':
            text = FONT.render('X', True, RED)
            rect = text.get_rect(center=(center_x, center_y))
            screen.blit(text, rect)
        elif value == 'o':
            text = FONT.render('O', True, BLUE)
            rect = text.get_rect(center=(center_x, center_y))
            screen.blit(text, rect)
        else:
            text = SMALL_FONT.render(str(value), True, GRAY)
            rect = text.get_rect(center=(center_x, center_y))
            screen.blit(text, rect)

    # info area
    pygame.draw.rect(screen, (245, 245, 245), (0, BOARD_SIZE, WIDTH, HEIGHT - BOARD_SIZE))

    turn_text = SMALL_FONT.render(f"Turn: {player.upper()}", True, BLACK)
    score_text = SMALL_FONT.render(
        f"Player X score: {winning_count[0]}   Player O score: {winning_count[1]}", True, BLACK
    )
    screen.blit(turn_text, (20, 620))
    screen.blit(score_text, (20, 660))

    if message:
        msg = BIG_FONT.render(message, True, GREEN)
        msg_rect = msg.get_rect(center=(WIDTH // 2, 705))
        screen.blit(msg, msg_rect)

    pygame.display.update()


def get_move_from_mouse(board, pos):
    x, y = pos

    if y >= BOARD_SIZE:
        return None

    col = x // CELL_SIZE
    row = y // CELL_SIZE
    position = row * 3 + col + 1

    if position in board:
        return position
    return None


def draw_play_again_buttons():
    yes_rect = pygame.Rect(120, 680, 140, 45)
    no_rect = pygame.Rect(340, 680, 140, 45)

    pygame.draw.rect(screen, GREEN, yes_rect)
    pygame.draw.rect(screen, RED, no_rect)

    yes_text = SMALL_FONT.render("Play Again", True, WHITE)
    no_text = SMALL_FONT.render("Quit", True, WHITE)

    screen.blit(yes_text, yes_text.get_rect(center=yes_rect.center))
    screen.blit(no_text, no_text.get_rect(center=no_rect.center))

    pygame.display.update()
    return yes_rect, no_rect


def wait_for_play_again():
    yes_rect, no_rect = draw_play_again_buttons()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if yes_rect.collidepoint(event.pos):
                    return True
                if no_rect.collidepoint(event.pos):
                    return False


# -----------------------
# GAME
# -----------------------
def play_game() -> None:
    board = create_board()
    print('Welcome to Tic-Tac-Toe')
    player = choose_beginner()
    winning_count = [0, 0]

    while True:
        board = create_board()
        round_over = False
        message = ""

        while True:
            draw_board(board, player, winning_count, message)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and not round_over:
                    position = get_move_from_mouse(board, event.pos)

                    if position is not None:
                        make_move(board, position, player)

                        if check_winner(board, player):
                            message = f"Player {player.upper()} wins!"
                            winning_count = player_winning_count(player, winning_count)
                            draw_board(board, player, winning_count, message)
                            round_over = True
                            break

                        if is_tie(board):
                            message = "It's a tie!"
                            draw_board(board, player, winning_count, message)
                            player = switch_player(player)  # if tie the last player does not begin
                            round_over = True
                            break

                        player = switch_player(player)

            if round_over:
                pygame.time.delay(800)
                if not wait_for_play_again():
                    print("GoodBye")
                    pygame.quit()
                    sys.exit()
                break


play_game()