import random as rnd
from TicTacToe.ElemCourse import ElemCourse
from TicTacToe.TicTacToe import TicTacToe


class Computer(object):
    """
    This class is designed to simulate the behavior of a computer in a game.
    """

    def __init__(self, data, game):
        """
        :param data: data of game, the basis of computer behavior
        :param game: TicTacToe class instance
        """
        self.data = data
        self.game = game
        self.win_cost = 1
        self.draw_cost = 0
        self.lose_cost = -1

    def build_count_matrix(self):
        """
        :return: matrix that contains data used for calculating chance matrix
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

        return count_matrix

    def build_chance_matrix(self, count_matrix):
        """
        :return: matrix that contains probability of victory for each cell
        """
        chance_matrix = [[self.draw_cost for _ in range(3)] for _ in range(3)]
        res_find_win_move, danger_elems = self.prepare_next_move()
        if res_find_win_move:
            chance_matrix[res_find_win_move.x][res_find_win_move.y] = self.win_cost
            return chance_matrix

        for i in range(3):
            for j in range(3):
                if ElemCourse(i, j) in self.game:
                    chance_matrix[i][j] = self.lose_cost - 1
                elif count_matrix[i][j][1] != 0:
                    chance_matrix[i][j] = count_matrix[i][j][0] / count_matrix[i][j][1]
        for elem in danger_elems:
            chance_matrix[elem.x][elem.y] = self.lose_cost

        # print(chance_matrix)
        return chance_matrix

    def learning_move(self):
        """
        The computer calculates the most successful move
        :return: ElemCourse class instance
        """
        count_matrix = self.build_count_matrix()
        chance_matrix = self.build_chance_matrix(count_matrix)

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
        Make a computer move
        """
        self.filter()  # leave games from self.data with same course of game
        random_move = rnd.random()
        if self.data and random_move >= probability_random:
            self.game.add(self.learning_move())
        else:
            self.game.add(self.generate_random_elem())

    def prepare_next_move(self):
        """

        :return: ElemCourse class instance if on next move will be victory (else None) \
        and danger_elems: matrix that contains elements on which through the course will be a loss if you go to them
        """
        res_find_win_move = self.game.find_win_move()
        danger_elems = []
        for elem in self.game.negative():
            continue_game = TicTacToe(self.game.copy())
            continue_game.move(elem)
            if continue_game.find_win_move():
                danger_elems.append(elem)

        return res_find_win_move, danger_elems

    def generate_random_elem(self):
        """
        Generate suitable ElemCourse class instance
        :return: ElemCourse class instance - empty field and current sign (O or X)
        """
        res_find_win_move, danger_elems = self.prepare_next_move()
        if res_find_win_move:
            return res_find_win_move

        selection = self.game.negative()
        if len(danger_elems) != len(selection):
            for elem in danger_elems:
                selection.remove(elem)
        return rnd.choice(selection)

    def filter(self):
        """
        filters the self.data, removing scripts that are not suitable for self.game
        :return:
        """
        if len(self.game) > 0:
            keys = set(self.data.keys())
            for key in keys:
                if key[:len(self.game)] != tuple(self.game):
                    self.data.pop(key)
