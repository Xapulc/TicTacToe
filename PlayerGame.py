from TicTacToe import TicTacToe
from FileWorker import load_dict_from_file
from ElemCourse import ElemCourse
from GenerateDataForGame import generate_random_elem


class PlayerGame(object):
    """
    A game with player,
    call start() to start game
    """

    def __init__(self):
        """
        1 An instance of the class is created for the game;
        2 Loading data for computer about previous games.
        """
        self.game = TicTacToe()
        self.data = load_dict_from_file("games2.txt")
        self.win = 1
        self.draw = 0
        self.lose = -1
        self.comp_turn = 0

    def start(self):
        """
        Start a game with computer
        """
        print("Welcome to TicTacToe, v. 2.7218281828459045")
        while True:
            while True:
                try:
                    who_first = input("Who if first: 0 - player, 1 - computer?")
                    assert who_first in ('0', '1')
                except AssertionError:
                    print("Please, write 0 or 1")
                else:
                    break

            self.comp_turn = int(who_first)
            while True:
                self.player_move() if self.comp_turn == 0 else self.comp_move()
                if self.game.winner() == 1:
                    print("You win!!!") if self.comp_turn == 0 else print("You lose")
                    print("Congratulations!!!")
                    break
                elif len(self.game) == 9:
                    print("Nobody win")
                    break

                self.comp_move() if self.comp_turn == 0 else self.player_move()
                if self.game.winner() == 0:
                    print("You lose") if self.comp_turn == 0 else print("You win!!!")
                    print("Congratulations!!!")
                    break

            agreement = input("Do you want to play new game: 1 - yes, other - no")
            if agreement == '1':
                print("Preparing...")
                self.game = TicTacToe()
                self.data = load_dict_from_file("games2.txt")
                continue
            else:
                break

    def player_move(self):
        """
        A player move,
        get user input (coordinate) like "1, 0" and set in this field O (zero)
        """
        while True:
            try:
                x, y = input("Your move(i.e. 1, 0): ").split(", ")
                move = ElemCourse(int(x), int(y))
                self.game.add(move)
            except ValueError:
                print("Too many or too little values or values aren't digital")
            except AssertionError:
                print("Values must be between 0 and 2")
            else:
                break

        print(self.game)

    def comp_move(self):
        """
        A computer move
        """
        self.game.filter(self.data)

        if self.data:
            self.game.add(self.learning_move())
        else:
            self.game.add(generate_random_elem(self.game))

        print(self.game)

    def learning_move(self):
        """
        The computer calculates the most successful move and return ElemCourse class instance
        :return: ElemCourse class instance
        """
        count_matrix = [[[0, 0] for _ in range(3)] for _ in range(3)]
        for game, res in self.data.items():
            move = game[len(self.game)]
            if res == self.comp_turn:  # win computer
                count_matrix[move.x][move.y][0] += self.win/(len(game)-len(self.game))**4
            elif res == 1 - self.comp_turn:  # win player
                count_matrix[move.x][move.y][0] += self.lose/(len(game)-len(self.game))**4
            else:
                count_matrix[move.x][move.y][0] += self.draw/(len(game)-len(self.game))**4
            count_matrix[move.x][move.y][1] += 1

        chance_matrix = [[self.draw for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                if count_matrix[i][j][1] != 0:
                    chance_matrix[i][j] = count_matrix[i][j][0] / count_matrix[i][j][1]
                elif ElemCourse(i, j) in self.game:
                    chance_matrix[i][j] = self.lose-1
        # print(chance_matrix)

        max = self.lose-1
        i_max = -1
        j_max = -1
        for i in range(3):
            for j in range(3):
                if chance_matrix[i][j] > max:
                    i_max = i
                    j_max = j
                    max = chance_matrix[i][j]

        return ElemCourse(i_max, j_max)


if __name__ == "__main__":
    game = PlayerGame()
    game.start()