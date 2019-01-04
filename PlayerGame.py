from TicTacToe import TicTacToe
from FileWorker import load_dict_from_file
from ElemCourse import ElemCourse
from GenerateDataForGame import generate_elem


class PlayerGame(object):

    def __init__(self):
        self.game = TicTacToe()
        self.data = load_dict_from_file()
        self.win = 1
        self.draw = 0
        self.lose = -1

    def start(self):
        print("Welcome to TicTacToe, v. 2.7218281828459045")
        input("Press Enter to start c:")

        while True:
            self.player_move()
            if self.game.winner() == 0:
                print("You win!!!")
                print("Congratulations!!!")
                break
            elif len(self.game) == 9:
                print("Nobody win")
                break

            self.comp_move()
            if self.game.winner() == 1:
                print("You lose")
                print("Congratulations!!!")
                break

    def player_move(self):
        while True:
            try:
                x, y = input("Your move(i.e. 1, 0): ").split(", ")
                move = ElemCourse(int(x), int(y), "o")
            except Exception:
                print("Wrong input")
                continue

            break

        self.game.append(move)
        print(self.game)

    def comp_move(self):
        keys = set(self.data.keys())
        for key in keys:
            if key[:len(self.game)] != tuple(self.game):
                self.data.pop(key)
        if self.data:
            self.game.append(self.__do_professional_move())
        else:
            self.game.append(generate_elem(self.game))

        print(self.game)

    def __do_professional_move(self):
        count_matrix = [[[0, 0] for _ in range(3)] for _ in range(3)]
        for game, res in self.data.items():
            move = game[len(self.game)]
            if res == 1:  # win "x"
                count_matrix[move.x][move.y][0] += self.win/(len(game)-len(self.game))**3
            elif res == 0:  # win "o"
                count_matrix[move.x][move.y][0] += self.lose/(len(game)-len(self.game))**3
            else:
                count_matrix[move.x][move.y][0] += self.draw/(len(game)-len(self.game))**3
            count_matrix[move.x][move.y][1] += 1

        chance_matrix = [[self.lose-1 if count_matrix[i][j][1] == 0 else count_matrix[i][j][0] / count_matrix[i][j][1]
                          for j in range(3)] for i in range(3)]
        print(chance_matrix)

        max = self.lose-1
        i_max = -1
        j_max = -1
        for i in range(3):
            for j in range(3):
                if chance_matrix[i][j] > max:
                    i_max = i
                    j_max = j
                    max = chance_matrix[i][j]

        return ElemCourse(i_max, j_max, "x")


if __name__ == "__main__":
    game = PlayerGame()
    game.start()