from core import FourInARow


def controller():

    game = FourInARow()

    game.new_game()
    print(f"{game.get_board()}\n")

    while not game.game_over:
        if game.turn_value == 0:
            game.turn(game.player_1)

        else:
            game.turn(game.player_2)

        print(f"{game.get_board()}\n")


if __name__ == '__main__':
    controller()
