import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 600, 750
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")

FONT = pygame.font.SysFont("arial", 36)
SMALL_FONT = pygame.font.SysFont("arial", 26)
BIG_FONT = pygame.font.SysFont("arial", 64)

BG_COLOR = (10, 10, 30)
LINE_COLOR = (255, 255, 255)
GLOW_COLOR = (100, 100, 255)
TEXT_COLOR = (255, 255, 255)
X_COLOR = (255, 100, 100)
O_COLOR = (100, 200, 255)
BUTTON_COLOR = (40, 40, 80)
BUTTON_HOVER = (70, 70, 130)

BOARD_TOP = 140
CELL_SIZE = 180
GRID_SIZE = CELL_SIZE * 3

CLOCK = pygame.time.Clock()


def num_input_validation() -> int:
    while True:
        try:
            num = int(input("enter number "))
            return num
        except ValueError as e:
            print(f'invalid {e}')


def choose_beginner() -> str:
    x = random.randint(0, 1)
    if x == 0:
        return 'x'
    return 'o'


def create_board() -> list:
    board = list(range(1, 9 + 1))
    return board


def print_board(board: list):
    for i in range(0, 9, 3):
        print(f"{board[i]} | {board[i + 1]} | {board[i + 2]}")
        print("---+---+---")


def get_move(board) -> int:
    while True:
        try:
            num = int(input("enter number "))
            if num == 999:
                if quit_game():
                    return 999
            if num in board:
                return num
            elif num != 999:
                print('please enter a valid input')
        except ValueError as e:
            print(f'invalid {e}, please enter a valid input')


def make_move(board, position, symbol):
    if symbol == 'x':
        board[position - 1] = 'x'
    else:
        board[position - 1] = 'o'


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


def show_scores(player, winning_count):
    if player == 'x':
        print(f'player x score: {winning_count[0]} player o score: {winning_count[1]}')
    else:
        print(f'player o score: {winning_count[1]} player x score: {winning_count[0]}')


def another_round() -> bool:
    while True:
        try:
            ans = int(input("enter 1 if you want another round or 0 if you want to quit "))
            match ans:
                case 1:
                    return True
                case 0:
                    return False
        except ValueError as e:
            print(f'invalid {e}, please enter a valid input')


def quit_game() -> bool:
    print("Are you sure you want to quit? this action will grant the other player a point")
    while True:
        answer = input("press 1 to continue playing or 0 to quit: ")
        if answer == '1':
            return False
        if answer == '0':
            return True
        print("please enter right input")


def get_available_moves(board: list) -> list:
    available = []
    for i in board:
        if isinstance(i, int):
            available.append(i)
    return available


def get_comp_move(board: list) -> int:
    available_moves = get_available_moves(board)
    random_index = random.randint(0, len(available_moves) - 1)
    return available_moves[random_index]


def choose_mode() -> int:
    while True:
        try:
            mode = int(input("enter 1 for 1v1 or 2 to play against to the computer: "))
            if mode in (1, 2):
                return mode
            print("please enter valid number")
        except ValueError as e:
            print(f'input needs to be a number {e}')


# ---------------- PYGAME UI HELPERS ----------------

def draw_glow_line(start, end, base_width=4):
    for width in (14, 10, 6):
        pygame.draw.line(SCREEN, GLOW_COLOR, start, end, width)
    pygame.draw.line(SCREEN, LINE_COLOR, start, end, base_width)


def draw_board(board, hover_cell=None):
    SCREEN.fill(BG_COLOR)

    title = BIG_FONT.render("Tic-Tac-Toe", True, TEXT_COLOR)
    SCREEN.blit(title, (WIDTH // 2 - title.get_width() // 2, 25))

    if hover_cell is not None:
        row = hover_cell // 3
        col = hover_cell % 3
        rect = pygame.Rect(col * CELL_SIZE, BOARD_TOP + row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(SCREEN, (30, 30, 70), rect, border_radius=18)

    for i in range(1, 3):
        x = i * CELL_SIZE
        draw_glow_line((x, BOARD_TOP), (x, BOARD_TOP + GRID_SIZE))
        y = BOARD_TOP + i * CELL_SIZE
        draw_glow_line((0, y), (GRID_SIZE, y))

    for i, value in enumerate(board):
        row = i // 3
        col = i % 3
        center_x = col * CELL_SIZE + CELL_SIZE // 2
        center_y = BOARD_TOP + row * CELL_SIZE + CELL_SIZE // 2

        if value == 'x':
            text = BIG_FONT.render("X", True, X_COLOR)
            SCREEN.blit(text, (center_x - text.get_width() // 2, center_y - text.get_height() // 2))
        elif value == 'o':
            text = BIG_FONT.render("O", True, O_COLOR)
            SCREEN.blit(text, (center_x - text.get_width() // 2, center_y - text.get_height() // 2))
        else:
            text = SMALL_FONT.render(str(value), True, (160, 160, 160))
            SCREEN.blit(text, (center_x - text.get_width() // 2, center_y - text.get_height() // 2))


def draw_status(player, winning_count, mode, message=""):
    mode_text = "1v1" if mode == 1 else "vs Computer"
    turn_text = FONT.render(f"Turn: {player.upper()}", True, TEXT_COLOR)
    score_text = SMALL_FONT.render(
        f"X: {winning_count[0]}    O: {winning_count[1]}    Mode: {mode_text}",
        True,
        TEXT_COLOR
    )

    SCREEN.blit(turn_text, (20, 95))
    SCREEN.blit(score_text, (20, 680))

    if message:
        msg = SMALL_FONT.render(message, True, (255, 220, 100))
        SCREEN.blit(msg, (20, 635))


def draw_button(rect, text, mouse_pos):
    color = BUTTON_HOVER if rect.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(SCREEN, color, rect, border_radius=14)
    pygame.draw.rect(SCREEN, LINE_COLOR, rect, 2, border_radius=14)
    txt = SMALL_FONT.render(text, True, TEXT_COLOR)
    SCREEN.blit(txt, (rect.centerx - txt.get_width() // 2, rect.centery - txt.get_height() // 2))


def get_clicked_cell(pos):
    x, y = pos
    if 0 <= x < GRID_SIZE and BOARD_TOP <= y < BOARD_TOP + GRID_SIZE:
        col = x // CELL_SIZE
        row = (y - BOARD_TOP) // CELL_SIZE
        return row * 3 + col
    return None


def choose_mode_pygame():
    button1 = pygame.Rect(120, 280, 360, 80)
    button2 = pygame.Rect(120, 400, 360, 80)

    while True:
        mouse_pos = pygame.mouse.get_pos()
        SCREEN.fill(BG_COLOR)

        title = BIG_FONT.render("Choose Mode", True, TEXT_COLOR)
        SCREEN.blit(title, (WIDTH // 2 - title.get_width() // 2, 130))

        draw_button(button1, "1v1", mouse_pos)
        draw_button(button2, "Play vs Computer", mouse_pos)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button1.collidepoint(event.pos):
                    return 1
                if button2.collidepoint(event.pos):
                    return 2

        CLOCK.tick(60)


def ask_another_round_pygame(message):
    yes_button = pygame.Rect(120, 430, 150, 70)
    no_button = pygame.Rect(330, 430, 150, 70)

    while True:
        mouse_pos = pygame.mouse.get_pos()
        SCREEN.fill(BG_COLOR)

        title = FONT.render(message, True, TEXT_COLOR)
        SCREEN.blit(title, (WIDTH // 2 - title.get_width() // 2, 250))

        draw_button(yes_button, "Play Again", mouse_pos)
        draw_button(no_button, "Quit", mouse_pos)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if yes_button.collidepoint(event.pos):
                    return True
                if no_button.collidepoint(event.pos):
                    return False

        CLOCK.tick(60)


def quit_game_pygame():
    yes_button = pygame.Rect(120, 430, 150, 70)
    no_button = pygame.Rect(330, 430, 150, 70)

    while True:
        mouse_pos = pygame.mouse.get_pos()
        SCREEN.fill(BG_COLOR)

        line1 = SMALL_FONT.render("Are you sure you want to quit?", True, TEXT_COLOR)
        line2 = SMALL_FONT.render("This action will grant the other player a point", True, TEXT_COLOR)

        SCREEN.blit(line1, (WIDTH // 2 - line1.get_width() // 2, 220))
        SCREEN.blit(line2, (WIDTH // 2 - line2.get_width() // 2, 270))

        draw_button(no_button, "Continue", mouse_pos)
        draw_button(yes_button, "Quit Round", mouse_pos)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if yes_button.collidepoint(event.pos):
                    return True
                if no_button.collidepoint(event.pos):
                    return False

        CLOCK.tick(60)


def get_move_pygame(board):
    while True:
        mouse_pos = pygame.mouse.get_pos()
        hover_cell = get_clicked_cell(mouse_pos)

        draw_board(board, hover_cell)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if quit_game_pygame():
                        return 999

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                cell = get_clicked_cell(event.pos)
                if cell is not None:
                    position = cell + 1
                    if position in board:
                        return position

        CLOCK.tick(60)


def play_game() -> None:
    print('Welcome to Tic-Tac-Toe')
    player = choose_beginner()
    mode = choose_mode_pygame()
    computer_symbol = 'o'
    winning_count = [0, 0]

    while True:
        board = create_board()
        round_over = False
        result_message = ""

        while not round_over:
            mouse_pos = pygame.mouse.get_pos()
            hover_cell = get_clicked_cell(mouse_pos)

            draw_board(board, hover_cell)
            draw_status(player, winning_count, mode, "Press ESC to exit round")
            pygame.display.flip()

            if mode == 2 and player == computer_symbol:
                pygame.time.delay(450)
                position = get_comp_move(board)
            else:
                position = get_move_pygame(board)

            if position == 999:
                player = switch_player(player)
                print(f'the player {player} wins')
                player_winning_count(player, winning_count)
                show_scores(player, winning_count)
                result_message = f"Player {player.upper()} wins! Other player quit."
                round_over = True
            else:
                make_move(board, position, player)

                if check_winner(board, player):
                    print(f'the player {player} wins')
                    winning_count = player_winning_count(player, winning_count)
                    show_scores(player, winning_count)
                    result_message = f"Player {player.upper()} wins!"
                    round_over = True

                elif is_tie(board):
                    print("it's a tie")
                    show_scores(player, winning_count)
                    result_message = "It's a tie!"
                    player = switch_player(player)
                    round_over = True

                else:
                    player = switch_player(player)

        end_waiting = True
        while end_waiting:
            draw_board(board)
            draw_status(player, winning_count, mode, result_message)
            pygame.display.flip()

            pygame.time.delay(900)
            end_waiting = False

        if not ask_another_round_pygame(result_message):
            break

    print("GoodBye")
    pygame.quit()
    sys.exit()


play_game()