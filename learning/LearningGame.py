from random import random

from players.Computer import Computer
from TicTacToe.TicTacToe import TicTacToe


class LearningGame(object):
    """
    A game between student-computer and teacher-computer,
    where teacher-computer learns by LearningTeacher,
    and student-computer learns by LearningStudent.
    """

    def __init__(self, teacher_dic, student_dic, start=None):
        """
        1. An instance of the class is created for the game;
        2. Loading data for computer about previous games.
        :param teacher_dic: teacher's experience
        :param student_dic: student's experience
        :param start: starting course of game
        """
        if start:
            self.game = start
        else:
            self.game = TicTacToe()
        self.teacher = Computer(teacher_dic, self.game)
        self.student = Computer(student_dic, self.game)
        self.student_turn = 1 if random() > 0.5 else 0  # if 1, student moves first, else teacher moves first

    def start(self, probability_random_move):
        """
        :param probability_random_move: chance of random move
        :return: course of game
        """
        while True:
            self.teacher.comp_move(probability_random_move) if self.student_turn == 0 \
                else self.student.comp_move(probability_random_move)
            if self.game.winner() == self.game.current_turn():
                break
            if len(self.game) == 9:  # field is filling
                break
        if self.student_turn == self.game.winner():
            status = 1
        elif self.student_turn == 1 - self.game.winner():
            status = -1
        else:
            status = 0
        return self.game, status
