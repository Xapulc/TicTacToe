from TicTacToe.TicTacToe import TicTacToe
from players.Player import Player


class GamePvP(object):
    """
    Game player vs player
    """

    def __init__(self):
        self.game = TicTacToe()
        self.playerOne = Player(self.game)
        self.playerTwo = Player(self.game)

    def start(self):
        print("Welcome to TicTacToe, v. 2.7218281828459045")
        while True:
            while True:
                print("First player move")
                self.playerOne.player_move()
                print(self.game)
                if self.game.winner() == 1:
                    print("First player win!!!")
                    print("Congratulations!!!")
                    break
                elif len(self.game) == 9:
                    print("Nobody wins")
                    break
                print("Second player move")
                self.playerTwo.player_move()
                print(self.game)
                if self.game.winner() == 0:
                    print("Second player win!!!")
                    print("Congratulations!!!")
                    break
            agreement = input("Do you want to play new game: 1 - yes, other - no")
            if agreement == '1':
                print("Preparing...")
                self.__init__()
                continue
            else:
                break


if __name__ == "__main__":
    game = GamePvP()
    game.start()


