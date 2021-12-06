import unittest

import numpy as np

from core import FourInARow, Player


class BoardTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.game = FourInARow()
        self.col_size = 7
        self.row_size = 6
        self.game.new_board(row_size=self.row_size, col_size=self.col_size)

    def test_new_board(self):
        board = self.game.new_board(row_size=self.row_size, col_size=self.col_size)

        self.assertEqual(len(board), 6)
        self.assertEqual(len(board[0]), 7)
        self.assertIsInstance(board, np.ndarray)

    def test_make_move(self):
        self.game.player_1 = Player(1, is_human=True, color="RED")
        self.game.player_1 = Player(2, is_human=False, color="YELLOW")
        print(self.board)
        self.assertEqual(len(self.board), 6)


if __name__ == '__main__':
    unittest.main()
