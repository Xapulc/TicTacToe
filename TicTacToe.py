import numpy as np


class TicTacToe:
    def __init__(self, course=None):
        if course is None:
            course = []
        self.__course = course

    def checkLine(self, index, value):
        return len([True for elem in self.__course
                    if (elem.x == index) and (elem.value == value)]) == 3

    def checkColumn(self, index, value):
        return len([True for elem in self.__course
                    if (elem.y == index) and (elem.value == value)]) == 3

    def checkGenDiag(self, value):
        return len([True for elem in self.__course
                    if (elem.x == elem.y) and (elem.value == value)]) == 3

    def checkSndDiag(self, value):
        return len([True for elem in self.__course
                    if (elem.x + elem.y == 2) and (elem.value == value)]) == 3

    def checkEnd(self, move):
        return self.checkLine(move.x, move.value) or \
               self.checkColumn(move.y, move.value) or \
               (move.onGenDiag()) and (self.checkGenDiag(move.value)) or \
               (move.onSndDiag()) and (self.checkSndDiag(move.value)) or \
               len(self.__course) == 9

    def move(self, move):
        def checkNewPoint(new):
            for elem in self.__course:
                assert (not elem == new)

        checkNewPoint(move)
        self.__course.append(move)
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

    def __iter__(self):
        return iter(self.__course)

    def __bool__(self):
        return bool(self.__course)

    def __getitem__(self, item):
        return self.__course[item]

    def __len__(self):
        return len(self.__course)

    def __str__(self):
        field = np.array([np.array([' ', ' ', ' ']) for _ in range(3)])
        for elem in self.__course:
            field[elem.x][elem.y] = 'x' if elem.value == 1 else 'o'

        line = "---"
        s = '\n'.join([''.join(l) for l in field])
        return f"{line}\n{s}\n{line}"
