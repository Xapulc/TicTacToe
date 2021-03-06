from TicTacToe.ElemCourse import ElemCourse


class Player(object):
    """
    Class that works with user
    """

    def __init__(self, game):
        """
        :param game: TicTacToe class instance
        """
        self.game = game

    def move(self):
        """
        A player move,
        get user input: (coordinate) like "1 0" and add it into game
        """
        while True:
            try:
                x, y = input("Your move(i.e. 1 0): ").split(" ")
                move = ElemCourse(int(x), int(y))
                self.game.add(move)
            except ValueError:
                print("Too many or too little values or values aren't digital")
            except AssertionError as err:
                print(err)
            else:
                break
