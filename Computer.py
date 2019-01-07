import random as rnd
from ElemCourse import ElemCourse


class Computer(object):

    def __init__(self, data, game):
        self.data = data
        self.game = game
        self.win_cost = 1
        self.draw_cost = 0
        self.lose_cost = -1

    def learning_move(self):
        """
        The computer calculates the most successful move and return ElemCourse class instance
        :return: ElemCourse class instance
        """
        turn = (len(self.game) + 1) % 2
        count_matrix = [[[0, 0] for _ in range(3)] for _ in range(3)]
        for game, res in self.data.items():
            move = game[len(self.game)]
            if res == turn:
                count_matrix[move.x][move.y][0] += self.win_cost / (len(game) - len(self.game))
            elif res == 1 - turn:
                count_matrix[move.x][move.y][0] += self.lose_cost / (len(game) - len(self.game))
            else:
                count_matrix[move.x][move.y][0] += self.draw_cost / (len(game) - len(self.game))
            count_matrix[move.x][move.y][1] += 1

        chance_matrix = [[self.draw_cost for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                if count_matrix[i][j][1] != 0:
                    chance_matrix[i][j] = count_matrix[i][j][0] / count_matrix[i][j][1]
                elif ElemCourse(i, j) in self.game:
                    chance_matrix[i][j] = self.lose_cost - 1
        # print(chance_matrix)

        max_val = self.lose_cost - 1
        i_max = -1
        j_max = -1
        for i in range(3):
            for j in range(3):
                if chance_matrix[i][j] > max_val:
                    i_max = i
                    j_max = j
                    max_val = chance_matrix[i][j]
        return ElemCourse(i_max, j_max)

    def comp_move(self, probability_random=0):
        """
        A computer move
        """
        self.filter()  # leave games from self.data with same course of game
        random_move = rnd.random()
        if self.data and random_move >= probability_random:
            self.game.add(self.learning_move())
        else:
            self.game.add(self.generate_random_elem())

    def generate_random_elem(self):
        """
        Generate suitable ElemCourse class instance
        :return: ElemCourse class instance - empty field and current sign (O or X)
        """
        return rnd.choice(self.game.negative())

    def filter(self):
        if len(self.game) > 0:
            keys = set(self.data.keys())
            for key in keys:
                if key[:len(self.game)] != tuple(self.game):
                    self.data.pop(key)
