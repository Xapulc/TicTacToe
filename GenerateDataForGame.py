import TicTacToe as ttt
import ElemCourse as el
import random as rnd


def generateElem(course):
    new = el.ElemCourse(rnd.randint(0, 2), rnd.randint(0, 2))
    while any(new.pointsEqual(elem) for elem in course):
        new = el.ElemCourse(rnd.randint(0, 2), rnd.randint(0, 2))

    if not course:
        new.value = 0
    else:
        new.value = 1 - course[len(course) - 1].value

    return new


def createRandomGame():
    game = ttt.TicTacToe()
    end = False
    while not end:
        end = game.move(generateElem(game.course))

    print(game)
    return game.course, game.winner()
