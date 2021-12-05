import sys
from typing import Union

import numpy as np


class Player:
    def __init__(self, value: int, is_human: bool, color: str):
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


class FourInARow:
    def __init__(self):
        self.player_1: Union[object, None] = None
        self.player_2: Union[object, None] = None
        self.col_size: Union[int, None] = None
        self.row_size: Union[int, None] = None
        self.board: Union[None, np.ndarray] = None
        self.game_over: bool = False
        self.turn_value: int = 0

    def generate_players(self, is_human: bool = False) -> None:
        self.player_1 = Player(1, is_human=True, color="RED")
        self.player_2 = Player(2, is_human=is_human, color="YELLOW")

    def new_board(self, col_size: int, row_size: int) -> np.ndarray:
        """
        Create new board with type: numpy array
        :return: numpy array
        """
        self.col_size = col_size
        self.row_size = row_size
        self.board = np.zeros((row_size, col_size))
        return self.board

    def make_move(self, value: int, col: int) -> None:
        if self.is_valid_location(col):
            row = self.generate_next_open_row(col)
            self.board[row][col] = value

    def turn(self, player):
        try:
            col = player.get_move()
            self.make_move(col=col, value=player.value)
            if self.winning_move(player.value):
                print("Player 1 wins")
                sys.exit()
        except ValueError:
            print("You entered an invalid number, please enter a number between 0 and 6")
            col = player.get_move()
            self.make_move(col=col, value=player.value)
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

    def get_board(self):
        return np.flip(self.board, 0)

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
