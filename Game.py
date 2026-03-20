import random

def choose_begginer() -> int:
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
    for i in range(1, 9 + 1, 3):
        print(f"{board[i]} | {board[i + 1]} | {board[i + 2]}")
        print("---+---+---")

def get_move(player, board) -> int:
    # the func will get legal move from the player(1-9, only available spots)
    # return: players choice

    pass

def make_move(board, position, symbol):
    # the func will update the board with the user's choice
    pass

def check_winner(board, symbol):
    # checks if there is a winner, and who is it
    pass

def is_tie(board) -> bool:
    # the func check if there's a tie
    pass

def switch_player(current):
    # the func will switch turns
    pass

def play_game() -> None:
    board = create_board()
    print('Welcome to Tic-Tac-Toe')

    player = choose_begginer()

    while True:
        print_board(board)
        print('place your symbol on the board')
        position = get_move(player, board)
        make_move(board, position, player)

        if check_winner(board, player) == True:
            print_board(board)
            print(f'the player {player} wins')
            break
        if is_tie() == True:
            print_board(board)
            print("it's a tie")
            break

        player = switch_player(player)


    pass
