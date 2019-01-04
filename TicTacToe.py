import numpy as np


class TicTacToe(list):

    def check_line(self, index, value):
        return len([True for i, elem in enumerate(self)
                    if (elem.x == index) and ((i + 1) % 2 == value)]) == 3

    def check_column(self, index, value):
        return len([True for i, elem in enumerate(self)
                    if (elem.y == index) and ((i + 1) % 2 == value)]) == 3

    def check_gen_diag(self, value):
        return len([True for i, elem in enumerate(self)
                    if (elem.x == elem.y) and ((i + 1) % 2 == value)]) == 3

    def check_snd_diag(self, value):
        return len([True for i, elem in enumerate(self)
                    if (elem.x + elem.y == 2) and ((i + 1) % 2 == value)]) == 3

    def check_end_with_move(self, move, value):
        return self.check_line(move.x, value) or \
               self.check_column(move.y, value) or \
               (move.on_gen_diag()) and (self.check_gen_diag(value)) or \
               (move.on_snd_diag()) and (self.check_snd_diag(value)) or \
               len(self) == 9

    def check_end(self):
        return (self.winner() != -1) or (len(self) == 9)

    def move(self, move):
        def check_new_point(new):
            for elem in self:
                assert (not elem == new)

        check_new_point(move)
        self.add(move)
        return self.check_end_with_move(move, len(self) % 2)

    def winner(self):
        for val in range(2):
            for i in range(3):
                if self.check_line(i, val):
                    return val
            for j in range(3):
                if self.check_column(j, val):
                    return val
            if self.check_gen_diag(val):
                return val
            if self.check_snd_diag(val):
                return val
        else:
            return -1  # nobody win

    def add(self, move):
        assert not move in self
        self.append(move)

    def __str__(self):
        field = [[' ' for _ in range(3)] for _ in range(3)]
        for i, elem in enumerate(self):
            field[elem.x][elem.y] = 'x' if (i + 1) % 2 == 1 else 'o'

        line = "---"
        s = '\n'.join([''.join(l) for l in field])
        return f"{line}\n{s}\n{line}"
