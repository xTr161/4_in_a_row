import math
import sys
from random import random, randint, choice
from typing import Union

import numpy as np


class Player:
    def __init__(self, value: int, is_human: bool, color: str, difficulty: int = None):
        self.difficulty: Union[None, int] = difficulty
        self.value: int = value
        self.is_human: bool = is_human
        self.color: str = color

    def get_move(self) -> int:
        move = None
        if self.is_human:
            move = int(input(f"Player {self.value}, Make your Selection(0-6):"))
            if move > 6 or move < 0:
                raise ValueError("Invalid move, please use a number between 0-6.")
        return move

    def ai_move(self):
        if not self.is_human:
            if self.difficulty == 1:
                move: int = randint(0, 6)
        return move

    def minimax(self, board, depth, alpha, beta, is_maximum):
        score = self.evaluate()

        # If Maximizer has won the game return his/her
        # evaluated score
        if score == 10:
            return score

        # If Minimizer has won the game return his/her
        # evaluated score
        if score == -10:
            return score

        # If there are no more moves and no winner then
        # it is a tie
        if not self.is_moves_left():
            return 0

        # If this maximizer's move
        if is_maximum:

            # print("calculating maximizers moves")
            best = -1000

            # Traverse all cells
            for i in range(4):
                for j in range(4):

                    # Check if cell is empty
                    if board[i][j] == '_':
                        # Make the move
                        board[i][j] = self.value

                        # Call minimax recursively and choose
                        # the maximum value
                        evaluation = self.minimax(board,
                                                  depth - 1, alpha, beta,
                                                  not is_maximum)
                        best = max(best, evaluation)
                        alpha = max(alpha, evaluation)
                        # Undo the move
                        board[i][j] = '_'
            return best

        # If this minimizer's move
        else:
            # print("calculating minimizers moves")
            best = 1000

            # Traverse all cells
            for i in range(4):
                for j in range(4):

                    # Check if cell is empty
                    if board[i][j] == '_':
                        # Make the move
                        board[i][j] = self.opponent
                        # Call minimax recursively and choose
                        # the minimum value
                        evaluation = self.minimax(board,
                                                  depth - 1, alpha, beta,
                                                  not is_maximum)
                        best = min(best, evaluation)
                        alpha = min(alpha, evaluation)
                        # Undo the move
                        board[i][j] = '_'
            return best


class FourInARow:
    def __init__(self):
        self.player_1: Union[object, None] = None
        self.player_2: Union[object, None] = None
        self.col_size: Union[int, None] = None
        self.row_size: Union[int, None] = None
        self.board: Union[None, np.ndarray] = None
        self.game_over: bool = False
        self.turn_value: int = 0
        PLAYER = 0
        AI = 1

        EMPTY = 0
        self.player_piece = 1
        self.ai_piece = 2

        self.window_length = 4

    def new_game(self) -> None:
        rows = int(input("Please enter row size"))
        column = int(input("Please enter column size"))
        self.new_board(row_size=rows, col_size=column)
        self.generate_players()

    def generate_players(self) -> None:
        self.player_1 = Player(1, is_human=True, color="RED")
        player2 = int(input("Who is player 2:\n1)Human\n2)Computer "))
        if player2 == 1:
            player2 = True
        elif player2 == 2:
            player2 = False
        else:
            raise ValueError("Player must be either computer or human:\nEnter 1 for Computer or 2 for Human opponent ")
        self.player_2 = Player(2, is_human=player2, color="YELLOW")

    def new_board(self, col_size: int, row_size: int) -> np.ndarray:
        """
        Create new board with type: numpy array
        :return: numpy array
        """
        if (col_size or row_size) < 4:
            raise ValueError("Minimum size for the board must be 4")
        else:
            self.col_size = col_size
            self.row_size = row_size
            self.board = np.zeros((row_size, col_size))
            return self.board

    def get_board(self):
        return np.flip(self.board, 0)

    def make_move(self, player_value: int, col: int) -> None:
        if self.is_valid_location(col):
            row: int = self.generate_next_open_row(col)
            self.board[row][col] = player_value

    def turn(self, player):
        try:
            if player.is_human:
                col: int = player.get_move()
                self.make_move(col=col, player_value=player.value)
                if self.winning_move(player.value):
                    print(f"Player {player.value} wins")
                    sys.exit()
            else:
                col: int = player.ai_move()
                self.make_move(col=col, player_value=player.value)
                if self.winning_move(player.value):
                    print(f"Player {player.value} wins")
                    sys.exit()
        except ValueError:
            print("You entered an invalid number, please enter a number between 0 and 6")
            col = player.get_move()
            self.make_move(col=col, player_value=player.value)
            if self.winning_move(player.value):
                print("Player 1 wins")
                sys.exit()
        self.turn_value += 1
        self.turn_value = self.turn_value % 2

    def is_valid_location(self, col: int) -> bool:
        return self.board[5][col] == 0

    def generate_next_open_row(self, col: int) -> int:
        for row in range(self.row_size):
            if self.board[row][col] == 0:
                return row

    def winning_move(self, player) -> bool:
        # Check horizontal locations for win
        for c in range(self.col_size - 3):
            for r in range(self.row_size):
                if self.board[r][c] == player and self.board[r][c + 1] == player and \
                        self.board[r][c + 2] == player and self.board[r][c + 3] == player:
                    return True

        # Check vertical locations for win
        for c in range(self.col_size):
            for r in range(self.row_size - 3):
                if self.board[r][c] == player and self.board[r + 1][c] == player and \
                        self.board[r + 2][c] == player and self.board[r + 3][c] == player:
                    return True

        # Check positively sloped diagonals
        for c in range(self.col_size - 3):
            for r in range(self.row_size - 3):
                if self.board[r][c] == player and self.board[r + 1][c + 1] == player and \
                        self.board[r + 2][c + 2] == player and \
                        self.board[r + 3][c + 3] == player:
                    return True

        # Check negatively sloped diagonals
        for c in range(self.col_size - 3):
            for r in range(3, self.row_size):
                if self.board[r][c] == player and self.board[r - 1][c + 1] == player and self.board[r - 2][
                    c + 2] == player and \
                        self.board[r - 3][c + 3] == player:
                    return True

    def get_valid_locations(self):
        valid_locations = []
        for col in range(self.col_size):
            if self.is_valid_location(col):
                valid_locations.append(col)
        return valid_locations

    def pick_best_move(self, piece):
        valid_locations = self.get_valid_locations()
        best_score = -10000
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = self.generate_next_open_row(col)
            temp_board = self.board.copy()
            drop_piece(temp_board, row, col, piece)
            score = score_position(temp_board, piece)
            if score > best_score:
                best_score = score
                best_col = col

        return best_col

    def score_position(self, board, piece):
        score = 0

        ## Score center column
        center_array = [int(i) for i in list(board[:, self.col_size // 2])]
        center_count = center_array.count(piece)
        score += center_count * 3

        ## Score Horizontal
        for r in range(self.row_size):
            row_array = [int(i) for i in list(board[r, :])]
            for c in range(self.col_size - 3):
                window = row_array[c:c + WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)

        ## Score Vertical
        for c in range(self.col_size):
            col_array = [int(i) for i in list(board[:, c])]
            for r in range(self.row_size - 3):
                window = col_array[r:r + WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)

        ## Score posiive sloped diagonal
        for r in range(self.row_size - 3):
            for c in range(self.col_size - 3):
                window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)

        for r in range(self.row_size - 3):
            for c in range(self.col_size - 3):
                window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)

        return score

    def is_terminal_node(self, board):
        return self.winning_move(board, self.player_piece) or self.winning_move(board, self.ai_piece) or len(
            self.get_valid_locations()) == 0

    def minimax(self, board, depth, alpha, beta, maximizingPlayer):
        valid_locations = self.get_valid_locations()
        is_terminal = self.is_terminal_node(board)
        if depth == 0 or is_terminal:
            if is_terminal:
                if self.winning_move(board, self.ai_piece):
                    return None, 100000000000000
                elif self.winning_move(board, self.player_piece):
                    return None, -10000000000000
                else:  # Game is over, no more valid moves
                    return None, 0
            else:  # Depth is zero
                return None, self.score_position(board, self.ai_piece)
        if maximizingPlayer:
            value = -math.inf
            column = choice(valid_locations)
            for col in valid_locations:
                row = self.generate_next_open_row(col)
                b_copy = board.copy()
                self.drop_piece(b_copy, row, col, self.ai_piece)
                new_score = self.minimax(b_copy, depth - 1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value

        else:  # Minimizing player
            value = math.inf
            column = choice(valid_locations)
            for col in valid_locations:
                row = self.generate_next_open_row(col)
                b_copy = board.copy()
                self.drop_piece(b_copy, row, col, self.player_piece)
                new_score = self.minimax(b_copy, depth - 1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value
