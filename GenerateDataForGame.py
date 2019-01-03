import TicTacToe as ttt
import ElemCourse as el
import random as rnd


def generateElem(game):
    new = el.ElemCourse(rnd.randint(0, 2), rnd.randint(0, 2))
    while new in game:
        new = el.ElemCourse(rnd.randint(0, 2), rnd.randint(0, 2))

    if not game:
        new.value = 0
    else:
        new.value = 1 - game[len(game) - 1].value

    return new


def createRandomGame():
    game = ttt.TicTacToe()
    end = False
    while not end:
        end = game.move(generateElem(game))

    print(game)
    return game, game.winner()
