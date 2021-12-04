# def find_best_move(board):
#     best_move = None
#     for current_move in board:
#         if current_move >= best_move:
#             best_move = current_move
# TODO: fix bug with x and O placement
from pprint import pprint


class FourInARow:
    def __init__(self):
        self.board: list = []
        self.player1: str = ""
        self.player2: str = ""
        self.game_over: bool = False
        self.player, self.opponent = 'x', 'o'
        self.no_rounds = 1

    def determine_players(self):
        self.player1 = "human"
        if self.player2 == "":
            determine_players = int(input("Who do you want to play against?\n1)Computer\n2)human\n"))
            if determine_players == 1:
                print("you have selected to play against the computer")
                self.player2 = "computer"
            elif determine_players == 2:
                print("you have selected to play against someone else")
                self.player2 = "human"
            else:
                if determine_players != (1 or 2):
                    raise ValueError("The value entered is invalid")

    def new_game(self) -> list:
        self.determine_players()
        self.board = [['_', '_', '_', '_'],
                       ['_', '_', '_', '_'],
                       ['_', '_', '_', '_'],
                       ['_', '_', '_', '_']]
        return self.board

    def make_move(self, player: str, move: tuple, ) -> list:
        place = ""
        if player == "human":
            place = "x"
        elif player == "computer":
            place = "O"
        if self.board[move[0]][move[1]] == "_":
            self.board[move[0]][move[1]] = place
        else:
            raise IndexError(" The move you are trying to make is on an illegal space")
        return self.board

    def turn(self, player) -> list:
        move = ()
        if player == "human":
            place_x = int(input("place x Axis: "))
            place_y = int(input("place y Axis: "))
            move = (place_x, place_y)

        elif player == "computer":
            best_move = self.find_best_move()
            move = (best_move[0], best_move[1])

        made_move = self.make_move(player=player, move=move)
        return made_move

    def round(self):
        print(f"Round {self.no_rounds}")
        players = [self.player1, self.player2]
        for player in players:
            self.turn(player)
            pprint(self.board)
            score = self.evaluate()
            self.is_winner(score=score)
        self.no_rounds += 1

    @staticmethod
    def get_winner(board_space: str) -> int:
        if board_space == "x":
            return 10
        elif board_space == "O":
            return -10

    def is_winner(self, score):
        if score == -10:
            print(f"O is the winner in {self.no_rounds}")
            self.game_over = True

        elif score == 10:
            print(f"X is the winner in {self.no_rounds}")
            self.game_over = True

    def evaluate(self) -> int:
        """
        Evaluates self.board to determine if a winner has been found
        :return: integer with a score used to identify the winning player
        """
        # TODO: simplify comparisons
        "Evaluate rows for a winning score"
        for row in range(0, 4):
            if self.board[row][0] == (self.board[row][1] and self.board[row][2] and self.board[row][3]):
                return self.get_winner(board_space=self.board[row][0])

        "Evaluate columns for a winning score"
        for col in range(0, 4):
            if self.board[0][col] == self.board[1][col] and self.board[1][col] == self.board[2][col] \
                    and self.board[2][col] == self.board[3][col]:
                return self.get_winner(board_space=self.board[0][col])

        "Evaluate right to left diagonal for a winning score"
        if self.board[0][0] == self.board[1][1] and self.board[1][1] == self.board[2][2] \
                and self.board[2][2] == self.board[3][3]:
            score = self.get_winner(board_space=self.board[0][0])
            return score

        "Evaluate left to right diagonal for a winning score"
        if self.board[0][3] == self.board[1][2] and self.board[1][2] == self.board[2][1] \
                and self.board[2][1] == self.board[3][0]:
            score = self.get_winner(board_space=self.board[3][0])
            return score

    def is_moves_left(self):
        for i in range(4):
            for j in range(4):
                if self.board[i][j] == '_':
                    return True
        return False

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
                        board[i][j] = self.player

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

    def find_best_move(self):
        best_val = -1000
        best_move = (-1, -1)

        # Traverse all cells, evaluate minimax function for
        # all empty cells. And return the cell with optimal
        # value.
        for i in range(4):
            for j in range(4):

                # Check if cell is empty
                if self.board[i][j] == '_':

                    # Make the move
                    self.board[i][j] = self.player

                    # compute evaluation function for this
                    # move.
                    move_val = self.minimax(self.board, 0, 0, 0, False)

                    # Undo the move
                    self.board[i][j] = '_'

                    # If the value of the current move is
                    # more than the best value, then update
                    # best/
                    if move_val > best_val:
                        best_move = (i, j)
                        best_val = move_val

        print("The value of the best Move is :", best_val)
        print()
        return best_move
