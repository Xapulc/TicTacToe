from utils import file_worker as fw
from learning.LearningGame import LearningGame


def create_learning_teacher_game():
    """
    :return: moves in the game and result (who winner)
    """
    game, _ = LearningGame({}, {}).start(1)
    return game, game.winner()


def learn_teacher(count):
    """
    :param count: number of games to be played by teacher with itself
    This script is used for learning teacher
    """
    dic = {}
    experience_path = "teacher_experience.txt"
    for i in range(count):
        game, res = create_learning_teacher_game()
        dic[tuple(game)] = res
        if count >= 100 and (i + 1) % (count // 100) == 0:
            print(f"complete on {100 * ((i + 1) / count):.0f}%")
    print(len(dic.keys()))
    fw.save_dict_to_file(dic, experience_path)

