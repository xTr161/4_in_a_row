import unittest
import numpy as np
from core import Board, Player


class BoardTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.game = Board(row_size=6, col_size=7)
        self.board = self.game.new_board()
        self.player1 = Player(value=1, is_human=True, color="RED")

    def test_new_board(self):
        board = self.game.new_board()

        self.assertEqual(len(board), 6)
        self.assertEqual(len(board[0]), 7)

    def test_make_move(self):
        self.game.make_move(self.player1, col=1)
        print(self.board)
        self.assertEqual(len(self.board), 6)


if __name__ == '__main__':
    unittest.main()
