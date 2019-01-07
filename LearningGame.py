from random import random

from GenerateDataForGame import generate_random_elem
from ElemCourse import ElemCourse
from TicTacToe import TicTacToe


class LearningGame(object):
    """
    A game between student computer and teacher computer,
    where teacher computer learns by LearningTeacher,
    and student computer learns by LearningStudent.
    """

    def __init__(self, teacher_dic, student_dic, start=None):
        """
        :param teacher_dic: teacher's experience
        :param student_dic: student's experience
        :param start: starting course of game
        1 An instance of the class is created for the game;
        2 Loading data for computer about previous games.
        """
        if not start:
            self.game = start
        else:
            self.game = TicTacToe()
        self.data_student = student_dic
        self.data_teacher = teacher_dic
        self.win = 1
        self.draw = 0
        self.lose = -1
        self.student_turn = 1 if random() > 0.5 else 0  # if 1, student moves first, else teacher moves first

    def start(self, probability_random_move):
        """
        :return: course of game
        """
        turn = (len(self.game) + 1) % 2

        while True:
            self.comp_move(turn, probability_random_move)
            if self.game.winner() == turn:
                break
            elif len(self.game) == 9:  # field is filling
                break

        return self.game

    def comp_move(self, turn, probability_random=0):
        """
        A computer move
        """
        games = self.data_student if turn == self.student_turn else self.data_teacher
        self.game.filter(games)  # leave games with same course of game

        random_move = random()
        if turn != self.student_turn:
            probability_random /= 10  # teacher has less prob. random move, then student

        if games and random_move > probability_random:
            self.game.add(self.learning_move(turn, games))
        else:
            self.game.add(generate_random_elem(self.game))

    def learning_move(self, turn, games):
        """
        The computer calculates the most successful move and return ElemCourse class instance
        :return: ElemCourse class instance
        """
        count_matrix = [[[0, 0] for _ in range(3)] for _ in range(3)]
        for game, res in games.items():
            move = game[len(self.game)]
            if res == turn:  # win computer
                count_matrix[move.x][move.y][0] += self.win / (len(game) - len(self.game))
            elif res == 1 - turn:  # win player
                count_matrix[move.x][move.y][0] += self.lose / (len(game) - len(self.game))
            else:
                count_matrix[move.x][move.y][0] += self.draw / (len(game) - len(self.game))
            count_matrix[move.x][move.y][1] += 1

        chance_matrix = [[self.draw for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                if count_matrix[i][j][1] != 0:
                    chance_matrix[i][j] = count_matrix[i][j][0] / count_matrix[i][j][1]
                elif ElemCourse(i, j) in self.game:
                    chance_matrix[i][j] = self.lose - 1
        # print(chance_matrix)

        max = self.lose - 1
        i_max = -1
        j_max = -1
        for i in range(3):
            for j in range(3):
                if chance_matrix[i][j] > max:
                    i_max = i
                    j_max = j
                    max = chance_matrix[i][j]

        return ElemCourse(i_max, j_max)