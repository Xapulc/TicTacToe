import numpy as np


class TicTacToe(list):

    def check_line(self, index, value):
        """
        :param index: line check index
        :param value: 0 (for O) or 1 (for X)
        :return: return true if line contains three O or X
        """
        return len([True for elem in self
                    if (elem.x == index) and (elem.value == value)]) == 3

    def check_column(self, index, value):
        """
        :param index: column check index
        :param value: 0 (for O) or 1 (for X)
        :return: return true if column contains three O or X
        """
        return len([True for elem in self
                    if (elem.y == index) and (elem.value == value)]) == 3

    def check_gen_diag(self, value):
        """
        :param value: 0 (for O) or 1 (for X)
        :return: return true if general diagonal contains three O or X
        """
        return len([True for elem in self
                    if (elem.x == elem.y) and (elem.value == value)]) == 3

    def check_snd_diag(self, value):
        """
        :param value: 0 (for O) or 1 (for X)
        :return: return true if secondary diagonal contains three O or X
        """
        return len([True for elem in self
                    if (elem.x + elem.y == 2) and (elem.value == value)]) == 3

    def check_end_with_move(self, move):
        """
        Checks whether the game is over after last move
        :param move: last move in the game
        :return: true uf game is end
        """
        return self.check_line(move.x, move.value) or \
               self.check_column(move.y, move.value) or \
               (move.on_gen_diag()) and (self.check_gen_diag(move.value)) or \
               (move.on_snd_diag()) and (self.check_snd_diag(move.value)) or \
               len(self) == 9

    def check_end(self):
        """
        Checks whether the game is over
        :return: true if game is end
        """
        return (self.winner() != -1) or (len(self) == 9)

    def move(self, move):
        """
        :param move: ElemCourse class instance, next move in game
        :return: true if game is over after this move
        """
        def check_new_point(new):
            for elem in self:
                assert (not elem == new)

        check_new_point(move)
        self.append(move)
        return self.check_end_with_move(move)

    def winner(self):
        """
        Checks whether there is a winner in the game at the moment
        :return: return 0 -> O - winner; 1 -> X - winner; -1 -> nobody win (dead heat or game isn't over)
        """
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
            return -1

    def __str__(self):
        field = np.array([np.array([' ', ' ', ' ']) for _ in range(3)])
        for elem in self:
            field[elem.x][elem.y] = 'x' if elem.value == 1 else 'o'

        line = "---"
        s = '\n'.join([''.join(l) for l in field])
        return f"{line}\n{s}\n{line}"
