from utils import file_worker as fw
from learning.LearningGame import LearningGame


def create_learning_teacher_game():
    """
    :return: moves in the game and result (who winner)
    """
    game, _ = LearningGame({}, {}).start(1)
    return game, game.winner()


if __name__ == "__main__":
    """This script is used for learning teacher"""
    count = 500
    dic = {}
    for i in range(count):
        game, res = create_learning_teacher_game()
        dic[tuple(game)] = res
        if (i+1) % (count // 100) == 0:
            print(f"complete on {100 * ((i+1)/count):.0f}%")
    print(len(dic.keys()))
    fw.save_dict_to_file(dic, "res/games.txt")
