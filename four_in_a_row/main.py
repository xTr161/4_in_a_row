from core import FourInARow


def controller():
    rows = int(input("Please enter row size"))
    column = int(input("Please enter column size"))

    game = FourInARow()
    player2 = int(input("Who is player 2:\n1)Human\n2)Computer "))
    if player2 == 1:
        player2 = True
    elif player2 == 2:
        player2 = False
    else:
        raise ValueError("Player must be either computer or human:\nEnter 1 for Computer or 2 for Human opponent ")
    game.generate_players(is_human=player2)
    game.new_board(row_size=rows, col_size=column)
    print(f"{game.get_board()}\n")

    while not game.game_over:
        if game.turn_value == 0:
            game.turn(game.player_1)

        else:
            game.turn(game.player_2)

        print(f"{game.get_board()}\n")


if __name__ == '__main__':
    controller()
