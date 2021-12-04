from core import FourInARow


def controller():
    game = FourInARow(row_size=6, col_size=7)
    game.new_board()

    while not game.game_over:
        # Ask for player 1 input
        if game.turn_value == 0:
            game.turn(game.player_1)
            print(game.get_board())

        # Ask for player 2 input
        else:
            game.turn(game.player_2)

        print(game.get_board())


if __name__ == '__main__':
    controller()
