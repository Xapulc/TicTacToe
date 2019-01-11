from players.Computer import Computer
from players.Player import Player
from TicTacToe.TicTacToe import TicTacToe
from utils.file_worker import load_dict_from_file, save_dict_to_file


class PlayerGame(object):
    """
    A game with player,
    call beginning_game() to begin game with player
    """

    def __init__(self):
        """
        1. An instance of the class is created for the game;
        2. Loading data for computer about previous games.
        """
        self.game = TicTacToe()
        self.player = Player(self.game)
        self.experience_path = "student_experience.txt"
        self.comp = Computer(load_dict_from_file(self.experience_path), self.game)
        self.comp_turn = 0

    def start(self):
        """
        Start a game with computer
        Main control thread of game
        """
        print("Welcome to TicTacToe, v. 2.7218281828459045")
        while True:
            while True:
                try:
                    who_first = input("Who first: 0 - player, 1 - computer?")
                    assert who_first in ('0', '1')
                except AssertionError:
                    print("Please, write 0 or 1")
                else:
                    break

            self.comp_turn = int(who_first)
            while True:
                self.player.player_move() if self.comp_turn == 0 else self.comp.comp_move()
                print(self.game)
                if self.game.winner() == 1:
                    print("You win!!!") if self.comp_turn == 0 else print("You lose")
                    print("Congratulations!!!")
                    break
                elif len(self.game) == 9:
                    print("Nobody win")
                    break

                self.comp.comp_move() if self.comp_turn == 0 else self.player.player_move()
                print(self.game)
                if self.game.winner() == 0:
                    print("You lose") if self.comp_turn == 0 else print("You win!!!")
                    print("Congratulations!!!")
                    break

            data = load_dict_from_file(self.experience_path)
            data[tuple(self.game)] = self.game.winner()
            save_dict_to_file(data, self.experience_path)

            agreement = input("Do you want to play new game: 1 - yes, other - no")
            if agreement == '1':
                print("Preparing...")
                self.__init__()
                continue
            else:
                break
