import random

def num_input_validation() -> int:
    # validates the input as int and returns the input
    while True:
        try:
            num = int(input("enter number "))
            return num
        except ValueError as e:
            print(f'invalid {e}')

def choose_beginner() -> str:
    # the func will return who is begins the game
    x = random.randint(0, 1)
    if x == 0:
        return 'x'
    return 'o'

def create_board() -> list:
    # the func will return a new empty board
    board = list(range(1,9 + 1))
    return board

def print_board(board: list):
    # the func will print the current board
    for i in range(0, 9, 3):
        print(f"{board[i]} | {board[i + 1]} | {board[i + 2]}")
        print("---+---+---")

def get_move(board) -> int:
    # the func will get legal move from the player(1-9, only available spots)
    # return: players choice

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
    # the func will update the board with the user's choice
    if symbol == 'x':
        board[position - 1] = 'x'
    else:
        board[position - 1] = 'o'


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
    if any(isinstance(i, int) for i in board): # isinstance checks if a value is a specific type
        return False
    return True

def switch_player(current):
    # the func will switch turns
    if current == 'o':
        return 'x'
    return 'o'

def player_winning_count(player, winning_count) -> list:
    # the function add one point to the current player score
    if player == 'x':
        winning_count[0] += 1
        return winning_count
    winning_count[1] += 1
    return winning_count

def show_scores(player, winning_count):
    # the function will print the current scores
    if player == 'x':
        print(f'player x score: {winning_count[0]} player o score: {winning_count[1]}')
    else:
        print(f'player o score: {winning_count[1]} player x score: {winning_count[0]}')

def another_round() -> bool:
    # the func will look if the player want another round
    while True:
        try:
            ans = int(input("enter 1 if you want another round or 0 if you want to quit "))
            match ans:
                case 1:
                    return True
                case 0:
                    return False
        except ValueError or ZeroDivisionError as e:
            print(f'invalid {e}, please enter a valid input')

def quit_game() -> bool:
    """
    the function makes sure if the user want to end his turn
    :return: True if he wants to quit False if to continue
    """
    print("Are you sure you want to quit? this action will grant the other player a point")
    while True:
        answer = input("press 1 to continue playing or 0 to quit: ")
        if answer == '1':
            return False
        if answer == '0':
            return True
        print("please enter right input")

def get_available_moves(board: list) -> list:
    """
    the function takes the current board and gives back available places on it
    :param board:
    :return: available indexes as list
    """
    available = []
    for i in board:
        if isinstance(i, int):
            available.append(i)
    return available

def get_comp_move(board: list) -> int:
    """
    the function looks at the current available moves and returns one random choice
    :param board:
    :return: computer choice as number
    """
    available_moves = get_available_moves(board)
    random_index = random.randint(0, len(available_moves) - 1)
    return available_moves[random_index]

def choose_mode() -> int:
    """
    the player chooses between the computer or 1v1
    :return: 1 for 1v1, 2 for computer
    """
    while True:
        try:
            mode = int(input("enter 1 for 1v1 or 2 to play against to the computer: "))
            if mode in (1, 2):
                return mode
            print("please enter valid number")
        except ValueError as e:
            print(f'input needs to be a number {e}')

def play_game() -> None:
    print('Welcome to Tic-Tac-Toe')
    player = choose_beginner()
    mode = choose_mode()
    computer_symbol = 'o'
    winning_count = [0, 0]

    while True:
        board = create_board()
        while True:
            print_board(board)
            print(f"It's {player} turn, place your symbol on the board, press 999 to exit")
            if mode == 2 and player == computer_symbol:
                position = get_comp_move(board)
                print(f'computer chose {position}')
            else:
                position = get_move(board)
            if position == 999:
                player = switch_player(player)
                print(f'the player {player} wins')
                player_winning_count(player, winning_count)
                show_scores(player, winning_count)
                break
            make_move(board, position, player)

            if check_winner(board, player):
                print_board(board)
                print(f'the player {player} wins')
                winning_count = player_winning_count(player, winning_count)
                show_scores(player, winning_count)
                break
            if is_tie(board):
                print_board(board)
                print("it's a tie")
                show_scores(player, winning_count)
                player = switch_player(player) # if tie the last player does not begin
                break
            player = switch_player(player)
        if not another_round():
            break
    print("GoodBye")


play_game()
