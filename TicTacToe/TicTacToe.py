from collections import deque
from threading import Thread
from time import time

from TicTacToe.ElemCourse import ElemCourse


class TicTacToe(list):
    def __check_line(self, index, value):
        """
        :param index: line check index
        :param value: the value on last move: 0 (for O) or 1 (for X)
        :return: return true if line contains three value
        """
        return len([True for i, elem in enumerate(self)
                    if (elem.x == index) and ((i + 1) % 2 == value)]) == 3

    def __check_column(self, index, value):
        """
        :param index: column check index
        :param value: the value on last move: 0 (for O) or 1 (for X)
        :return: return true if column contains three O or X
        """
        return len([True for i, elem in enumerate(self)
                    if (elem.y == index) and ((i + 1) % 2 == value)]) == 3

    def __check_gen_diag(self, value):
        """
        :param value: 0 (for O) or 1 (for X)
        :return: the value on last move: 0 (for O) or 1 (for X)
        """
        return len([True for i, elem in enumerate(self)
                    if (elem.x == elem.y) and ((i + 1) % 2 == value)]) == 3

    def __check_snd_diag(self, value):
        """
        :param value: the value on last move: 0 (for O) or 1 (for X)
        :return: return true if secondary diagonal contains three O or X
        """
        return len([True for i, elem in enumerate(self)
                    if (elem.x + elem.y == 2) and ((i + 1) % 2 == value)]) == 3

    def __check_end_with_move(self, move, value):
        """
        Checks whether the game is over after last move
        :param move: last move in the game
        :return: true uf game is end
        """
        return self.__check_line(move.x, value) or \
               self.__check_column(move.y, value) or \
               (move.on_gen_diag()) and (self.__check_gen_diag(value)) or \
               (move.on_snd_diag()) and (self.__check_snd_diag(value)) or \
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
        return self.__check_end_with_move(move, self.last_turn)

    def best_move(self):
        """
        Recursively find the best move
        :return: move and res, -1 -> lose; 0 -> draw; 1 -> win
        """
        def helper(game, next_move, results):
            game.add(next_move)

            if game.check_end():
                if game.winner() == -1:
                    results.append((next_move, draw))
                elif game.winner() == self.current_turn:
                    results.append((next_move, win))
                else:
                    results.append((next_move, lose))
            else:
                move, res = game.best_move()
                results.append((next_move, -res))

        win = 1
        draw = 0
        lose = -1
        max_deep = 1
        best_move = None
        best_res = lose-1
        results = deque()
        count = len(self.negative())

        threads = {}
        # start = time()
        for elem in self.negative():
            if len(self) < max_deep:
                threads[elem] = Thread(target=helper, args=[TicTacToe(self.copy()), elem, results])
                threads[elem].start()
            else:
                helper(TicTacToe(self.copy()), elem, results)

        while count > 0:
            if len(results) > 0:
                count -= 1
                (move, res) = results.popleft()
                if res > best_res:
                    best_move, best_res = move, res

        # end = time()
        # if len(self) < 3:
        #     print(f"time on lvl {len(self)} = {end-start}")

        return best_move, best_res

    @property
    def current_turn(self):
        """
        :return: who should move now, 0 -> O; 1 -> X
        """
        return (len(self) + 1) % 2

    @property
    def last_turn(self):
        """
        :return: who moved last, 0 -> O; 1 -> X
        """
        return 1 - self.current_turn

    def winner(self):
        """
        Checks whether there is a winner in the game at the moment
        :return: return 0 -> O - winner; 1 -> X - winner; -1 -> nobody win (dead heat or game isn't over)
        """
        last = self[len(self) - 1]
        if self.__check_line(last.x, self.last_turn) or self.__check_column(last.y, self.last_turn) \
                or self.__check_gen_diag(self.last_turn) or self.__check_snd_diag(self.last_turn):
            return self.last_turn
        else:
            return -1

    def add(self, move):
        """
        Added new move in game
        :param move: ElemCourse class instance
        """
        assert move not in self, "Cell isn't empty"
        self.append(move)

    def find_win_move(self):
        """
        Searching winner move (else return none)
        :return:
        """
        if len(self) == 9:
            return None

        for elem in self.negative():
            continue_game = TicTacToe(self.copy())
            continue_game.move(elem)
            if continue_game.winner() != -1:
                return elem
        return None

    def negative(self):
        """
        :return: list than contains empty cells in game
        """
        res = []
        for i in range(3):
            for j in range(3):
                if not ElemCourse(i, j) in self:
                    res.append(ElemCourse(i, j))
        return res

    def __str__(self):
        field = [[' ' for _ in range(3)] for _ in range(3)]
        for i, elem in enumerate(self):
            field[elem.x][elem.y] = 'x' if (i + 1) % 2 == 1 else 'o'

        line = "---"
        s = '\n'.join([''.join(l) for l in field])
        return f"{line}\n{s}\n{line}"
