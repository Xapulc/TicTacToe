import numpy as np


class TicTacToe:
    def __init__(self, course=[]):
        self.course = course

    def checkLine(self, index, value):
        return len([True for elem in self.course
                    if (elem.x == index) and (elem.value == value)]) == 3

    def checkColumn(self, index, value):
        return len([True for elem in self.course
                    if (elem.y == index) and (elem.value == value)]) == 3

    def checkGenDiag(self, value):
        return len([True for elem in self.course
                    if (elem.x == elem.y) and (elem.value == value)]) == 3

    def checkSndDiag(self, value):
        return len([True for elem in self.course
                    if (elem.x + elem.y == 2) and (elem.value == value)]) == 3

    def checkEnd(self, move):
        if self.checkLine(move.x, move.value):
            return True
        elif self.checkColumn(move.y, move.value):
            return True
        elif (move.onGenDiag()) and (self.checkGenDiag(move.value)):
            return True
        elif (move.onSndDiag()) and (self.checkSndDiag(move.value)):
            return True
        else:
            return len(self.course) == 9

    def move(self, move):
        def checkNewPoint(new):
            for elem in self.course:
                assert (not elem.pointsEqual(new))

        checkNewPoint(move)
        self.course.append(move)
        return self.checkEnd(move)

    def winner(self):
        for val in range(2):
            for i in range(3):
                if self.checkLine(i, val):
                    return val
            for j in range(3):
                if self.checkColumn(j, val):
                    return val
            if self.checkGenDiag(val):
                return val
            if self.checkSndDiag(val):
                return val
        else:
            return -1  # nobody doesn't win

    def __str__(self):
        field = np.array([np.array([' ', ' ', ' ']) for _ in range(3)])
        for elem in self.course:
            field[elem.x][elem.y] = 'x' if elem.value == 1 else 'o'
        return f'''{''.join(field[0])}\n{''.join(field[1])}\n{''.join(field[2])}'''
