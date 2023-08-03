def initialize_board():
    return [' '] * 9

def print_board(board):
    print("-------------")
    for i in range(3):
        print(f"| {board[i * 3]} | {board[i * 3 + 1]} | {board[i * 3 + 2]} |")
        print("-------------")

def is_board_full(board):
    return ' ' not in board

def check_winner(board, player):
    win_patterns = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]             # Diagonals
    ]

    for pattern in win_patterns:
        if all(board[i] == player for i in pattern):
            return True
    return False

def check_draw(board):
    return is_board_full(board) and not check_winner(board, 'X') and not check_winner(board, 'O')

def get_player_move(board):
    while True:
        try:
            move = int(input("Enter your move (1-9): "))
            if 1 <= move <= 9 and board[move - 1] == ' ':
                return move - 1
            else:
                print("Invalid move. Try again.")
        except ValueError:
            print("Invalid input. Try again.")

def play_game():
    board = initialize_board()
    current_player = 'X'

    while True:
        print_board(board)

        if check_winner(board, 'X'):
            print("Player X wins!")
            break
        elif check_winner(board, 'O'):
            print("Player O wins!")
            break
        elif check_draw(board):
            print("It's a draw!")
            break

        if current_player == 'X':
            move = get_player_move(board)
        else:
            move = minimax(board, 'O')['index']

        board[move] = current_player
        current_player = 'X' if current_player == 'O' else 'O'

def minimax(board, player):
    available_moves = [i for i, spot in enumerate(board) if spot == ' ']

    if check_winner(board, 'X'):
        return {'score': -10}
    elif check_winner(board, 'O'):
        return {'score': 10}
    elif len(available_moves) == 0:
        return {'score': 0}

    moves = []
    for move in available_moves:
        new_board = board.copy()
        new_board[move] = player

        if player == 'O':
            result = minimax(new_board, 'X')
            result['index'] = move
            moves.append(result)
        else:
            result = minimax(new_board, 'O')
            result['index'] = move
            moves.append(result)

    if player == 'O':
        best_move = max(moves, key=lambda x: x['score'])
    else:
        best_move = min(moves, key=lambda x: x['score'])

    return best_move

if __name__ == "__main__":
    play_game()
