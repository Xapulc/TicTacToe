from TicTacToe.ElemCourse import ElemCourse


class Player(object):

    def __init__(self, game):
        self.game = game

    def player_move(self):
        """
        A player move,
        get user input (coordinate) like "1, 0" and set in this field O (zero)
        """
        while True:
            try:
                x, y = input("Your move(i.e. 1 0): ").split(" ")
                move = ElemCourse(int(x), int(y))
                self.game.add(move)
            except ValueError:
                print("Too many or too little values or values aren't digital")
            except AssertionError:
                print("Values must be between 0 and 2")
            else:
                break
