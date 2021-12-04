import unittest
from pprint import pprint

from core import FourInARow


class MyTestCase(unittest.TestCase):
    def setUp(cls) -> None:
        cls.game = FourInARow()
        cls.player1 = "human"
        cls.player2 = "computer"
        cls.game.player2 = cls.player2

    def test_new_game(self):
        self.game.new_game()
        empty_board = [['_', '_', '_', '_'],
                       ['_', '_', '_', '_'],
                       ['_', '_', '_', '_'],
                       ['_', '_', '_', '_']]

        self.assertEqual(self.game.player1, "human")
        self.assertEqual(self.game.player2, "computer")
        self.assertEqual(self.game.board, empty_board)
        self.assertIsInstance(self.game.board, list)
        self.assertEqual(self.game.game_over, False)

    def test_make_move(self):
        self.game.new_game()
        move = (0, 0)
        made_move = self.game.make_move(player=self.player1, move=move)
        mocked_board = [['x', '_', '_', '_'],
                        ['_', '_', '_', '_'],
                        ['_', '_', '_', '_'],
                        ['_', '_', '_', '_']]
        self.assertEqual(mocked_board, made_move)

    def test_turn(self):
        self.game.player2 = "computer"
        self.game.new_game()
        mocked_board = [['x', '_', '_', '_'],
                        ['_', '_', '_', '_'],
                        ['_', '_', '_', '_'],
                        ['_', '_', '_', '_']]
        made_move = self.game.turn(player=self.player1)

        self.assertEqual(self.game.no_rounds, 1)
        self.assertIsInstance(made_move, list)
        self.assertEqual(mocked_board[0][0], made_move[0][0])


if __name__ == '__main__':
    unittest.main()
