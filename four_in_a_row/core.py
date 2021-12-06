import math
import sys
from random import randint, choice
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

    # def ai_move(self):
    #     if not self.is_human:
    #         if self.difficulty == 1:
    #             return randint(0, 6)


class FourInARow:
    def __init__(self):
        self.player_1: Union[object, None] = None
        self.player_2: Union[object, None] = None
        self.col_size: Union[int, None] = None
        self.row_size: Union[int, None] = None
        self.board: Union[None, np.ndarray] = None
        self.game_over: bool = False
        self.turn_value: int = 0

        self.player_piece = 1
        self.ai_piece = 2
        self.window_length = 4

    def new_game(self) -> None:
        """
        Creates new game with user input for the column and row sizing
        :return:
        """
        rows = int(input("Please enter row size"))
        column = int(input("Please enter column size"))
        self.new_board(row_size=rows, col_size=column)
        self.generate_players()

    def generate_players(self) -> None:
        """
        Generate player 1 and player 2 and assign player 2 either as human or computer
        :return: void/None
        """
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
        """
        return the board by flipping the array, since the array ois reversed
        :return: np.array
        """
        return np.flip(self.board, 0)

    def make_move(self, player_value: int, col: int) -> None:
        """
        Takes player value and column and calls the generate next row method to allow placing of the value in the
        selected column
        :param player_value: determined by the player object value( either 1 or 2)
        :param col: the column as passed by the player
        :return: void/None
        """
        if self.is_valid_location(col):
            row: int = self.generate_next_open_row(col)
            self.board[row][col] = player_value

    def turn(self, player) -> None:
        """
        Invokes a turn based system to allow either user input or AI input
        :param player:
        :return:
        """
        try:
            if player.is_human:
                col: int = player.get_move()
                self.make_move(col=col, player_value=player.value)
                if self.winning_move(player.value):
                    print(f"Player {player.value} wins")
                    sys.exit()
            else:
                col, minimax_score = self.minimax(self.board, 5, -math.inf, math.inf, True)
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
        """
        Checks whether the column is a valid location
        :param col: integer for the column
        :return: boolean
        """
        return self.board[5][col] == 0

    def generate_next_open_row(self, col: int) -> int:
        """
        Generator to determine the next available row where the value is not 0
        :param col: integer
        :return: integer
        """
        for row in range(self.row_size):
            if self.board[row][col] == 0:
                return row

    def winning_move(self, player) -> bool:
        """
        Conditionals to check if the a winning combination has been made
        :param player:
        :return:
        """
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

    def get_valid_locations(self) -> list:
        """
        Get a list of possible valid locations, list is used by the AI
        :return: list of integers
        """
        valid_locations = []
        for col in range(self.col_size):
            if self.is_valid_location(col):
                valid_locations.append(col)
        return valid_locations

    def pick_best_move(self, piece):
        """

        :param piece:
        :return:
        """
        valid_locations = self.get_valid_locations()
        best_score = -10000
        best_col = choice(valid_locations)
        for col in valid_locations:
            row = self.generate_next_open_row(col)
            temp_board = self.board.copy()
            self.drop_piece(temp_board, row, col, piece)
            score = self.score_position(temp_board, piece)
            if score > best_score:
                best_score = score
                best_col = col

        return best_col

    def score_position(self, board: list, piece) -> int:
        score = 0

        # Score center column
        center_array = [int(i) for i in list(board[:, self.col_size // 2])]
        center_count = center_array.count(piece)
        score += center_count * 3

        # Score Horizontal
        for r in range(self.row_size):
            row_array = [int(i) for i in list(board[r, :])]
            for c in range(self.col_size - 3):
                window = row_array[c:c + self.window_length]
                score += self.evaluate_window(window, piece)

        # Score Vertical
        for c in range(self.col_size):
            col_array = [int(i) for i in list(board[:, c])]
            for r in range(self.row_size - 3):
                window = col_array[r:r + self.window_length]
                score += self.evaluate_window(window, piece)

        # Score positive sloped diagonal
        for r in range(self.row_size - 3):
            for c in range(self.col_size - 3):
                window = [board[r + i][c + i] for i in range(self.window_length)]
                score += self.evaluate_window(window, piece)

        for r in range(self.row_size - 3):
            for c in range(self.col_size - 3):
                window = [board[r + 3 - i][c + i] for i in range(self.window_length)]
                score += self.evaluate_window(window, piece)

        return score

    def is_terminal_node(self):
        return self.winning_move(self.player_piece) or self.winning_move(self.ai_piece) or len(
            self.get_valid_locations()) == 0

    def evaluate_window(self, window, piece):
        score = 0
        opp_piece = self.player_piece
        if piece == self.player_piece:
            opp_piece = self.ai_piece

        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(0) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(0) == 2:
            score += 2

        if window.count(opp_piece) == 3 and window.count(0) == 1:
            score -= 4

        return score

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        valid_locations = self.get_valid_locations()
        is_terminal = self.is_terminal_node()
        if depth == 0 or is_terminal:
            if is_terminal:
                if self.winning_move(self.ai_piece):
                    return None, 100000000000000
                elif self.winning_move(self.player_piece):
                    return None, -10000000000000
                else:  # Game is over, no more valid moves
                    return None, 0
            else:  # Depth is zero
                return None, self.score_position(board, self.ai_piece)
        if maximizing_player:
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

    @staticmethod
    def drop_piece(board, row, col, piece):
        board[row][col] = piece
