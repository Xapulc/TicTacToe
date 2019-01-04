from TicTacToe import TicTacToe
from ElemCourse import ElemCourse
from random import randint


def generate_elem(game):
    new = ElemCourse(randint(0, 2), randint(0, 2))
    while new in game:
        new = ElemCourse(randint(0, 2), randint(0, 2))

    return new


def create_random_game():
    game = TicTacToe()
    end = False
    while not end:
        end = game.move(generate_elem(game))

    # print(game)
    return game, game.winner()
