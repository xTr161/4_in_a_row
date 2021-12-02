# def find_best_move(board):
#     best_move = None
#     for current_move in board:
#         if current_move >= best_move:
#             best_move = current_move
def get_winner(board_space: str) -> int:
    if board_space == "x":
        return 10
    elif board_space == "0":
        return -10


def evaluate(board: list) -> int:
    """
    Evaluates teh board to determine if a winner has been found
    :param board: a matrix of a list within a list
    :return: integer with a score used to identify the winning player
    """
    "Evaluate rows for a winning score"
    for row in range(0, 4):
        if board[row][0] == board[row][1] and board[row][1] == board[row][2]:
            return get_winner(board_space=board[row][0])

    "Evaluate columns for a winning score"
    for col in range(0, 4):
        if board[0][col] == board[0][col] and board[0][col] == board[0][col]:
            return get_winner(board_space=board[0][col])
    "Evaluate diagonals for a winning score"
    if board[0][0] == board[1][1] and board[1][1] == board[2][2] and board[2][2] == board[3][3]:
        score = get_winner(board_space=board[0][0])
        return score

    if board[0][3] == board[1][2] and board[1][2] == board[2][1] and board[2][2] == board[3][0]:
        score = get_winner(board_space=board[3][0])
        return score

    return 0


if __name__ == '__main__':
    board = [['x', '_', 'o', 'o'],
             ['_', 'x', 'o', 'o'],
             ['_', '_', 'x', 'o'],
             ['_', '_', 'o', 'o']]

    value = evaluate(board)
    print("The value of this board is", value)
