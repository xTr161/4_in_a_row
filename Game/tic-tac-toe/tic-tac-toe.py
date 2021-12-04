import sys
from pprint import pprint

from core import FourInARow


def main():
    try:
        game = FourInARow()
        game.new_game()
        pprint(game.board)
        while not game.game_over:
            game.round()
            continue
    except KeyboardInterrupt:
        sys.exit()


if __name__ == '__main__':
    main()
