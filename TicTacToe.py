from ElemCourse import ElemCourse


class TicTacToe(list):
    def check_line(self, index, value):
        """
        :param index: line check index
        :param value: 0 (for O) or 1 (for X)
        :return: return true if line contains three O or X
        """
        return len([True for i, elem in enumerate(self)
                    if (elem.x == index) and ((i + 1) % 2 == value)]) == 3

    def check_column(self, index, value):
        """
        :param index: column check index
        :param value: 0 (for O) or 1 (for X)
        :return: return true if column contains three O or X
        """
        return len([True for i, elem in enumerate(self)
                    if (elem.y == index) and ((i + 1) % 2 == value)]) == 3

    def check_gen_diag(self, value):
        """
        :param value: 0 (for O) or 1 (for X)
        :return: return true if general diagonal contains three O or X
        """
        return len([True for i, elem in enumerate(self)
                    if (elem.x == elem.y) and ((i + 1) % 2 == value)]) == 3

    def check_snd_diag(self, value):
        """
        :param value: 0 (for O) or 1 (for X)
        :return: return true if secondary diagonal contains three O or X
        """
        return len([True for i, elem in enumerate(self)
                    if (elem.x + elem.y == 2) and ((i + 1) % 2 == value)]) == 3

    def check_end_with_move(self, move, value):
        """
        Checks whether the game is over after last move
        :param move: last move in the game
        :return: true uf game is end
        """
        return self.check_line(move.x, value) or \
               self.check_column(move.y, value) or \
               (move.on_gen_diag()) and (self.check_gen_diag(value)) or \
               (move.on_snd_diag()) and (self.check_snd_diag(value)) or \
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
        self.add(move)
        return self.check_end_with_move(move, len(self) % 2)

    def learning_move(self, turn, games, win_cost, draw_cost, lose_cost):
        """
        The computer calculates the most successful move and return ElemCourse class instance
        :return: ElemCourse class instance
        """
        count_matrix = [[[0, 0] for _ in range(3)] for _ in range(3)]
        for game, res in games.items():
            move = game[len(self.game)]
            if res == turn:  # win computer
                count_matrix[move.x][move.y][0] += win_cost / (len(game) - len(self))
            elif res == 1 - turn:  # win player
                count_matrix[move.x][move.y][0] += lose_cost / (len(game) - len(self))
            else:
                count_matrix[move.x][move.y][0] += draw_cost / (len(game) - len(self))
            count_matrix[move.x][move.y][1] += 1

        chance_matrix = [[draw_cost for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                if count_matrix[i][j][1] != 0:
                    chance_matrix[i][j] = count_matrix[i][j][0] / count_matrix[i][j][1]
                elif ElemCourse(i, j) in game:
                    chance_matrix[i][j] = lose_cost - 1
        # print(chance_matrix)

        max = lose_cost - 1
        i_max = -1
        j_max = -1
        for i in range(3):
            for j in range(3):
                if chance_matrix[i][j] > max:
                    i_max = i
                    j_max = j
                    max = chance_matrix[i][j]

        return ElemCourse(i_max, j_max)

    def winner(self):
        """
        Checks whether there is a winner in the game at the moment
        :return: return 0 -> O - winner; 1 -> X - winner; -1 -> nobody win (dead heat or game isn't over)
        """
        last, turn = self[len(self) - 1], len(self) % 2
        if self.check_line(last.x, turn) or self.check_column(last.y, turn) \
                or self.check_gen_diag(turn) or self.check_snd_diag(turn):
            return turn
        else:
            return -1

    def add(self, move):
        assert not move in self
        self.append(move)

    def negative(self):
        res = []
        for i in range(3):
            for j in range(3):
                if not ElemCourse(i, j) in self:
                    res.append(ElemCourse(i, j))
        return res

    def filter(self, games):
        if len(self) > 0:
            keys = set(games.keys())
            for key in keys:
                if key[:len(self)] != tuple(self):
                    games.pop(key)

    def __str__(self):
        field = [[' ' for _ in range(3)] for _ in range(3)]
        for i, elem in enumerate(self):
            field[elem.x][elem.y] = 'x' if (i + 1) % 2 == 1 else 'o'

        line = "---"
        s = '\n'.join([''.join(l) for l in field])
        return f"{line}\n{s}\n{line}"
