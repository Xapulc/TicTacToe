import TicTacToe as ttt
import ElemCourse as el
import random as rnd


def generate_elem(game):
    new = el.ElemCourse(rnd.randint(0, 2), rnd.randint(0, 2))
    while new in game:
        new = el.ElemCourse(rnd.randint(0, 2), rnd.randint(0, 2))

    if not game:
        new.value = 0
    else:
        new.value = 1 - game[len(game) - 1].value

    return new


def create_random_game():
    game = ttt.TicTacToe()
    end = False
    while not end:
        end = game.move(generate_elem(game))

    print(game)
    return game, game.winner()
