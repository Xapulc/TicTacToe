import random as rnd


def generate_random_elem(game):
    """
    Generate suitable ElemCourse class instanse
    :param game: current game
    :return: ElemCourse class instance - empty field and current sign (O or X)
    """

    return rnd.choice(game.negative())