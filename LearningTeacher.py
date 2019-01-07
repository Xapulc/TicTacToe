import GenerateDataForGame as gd
import FileWorker as fw
from TicTacToe import TicTacToe


def create_learning_teacher_game():
    """
    :return: moves in the game and result (who winner)
    """
    game = TicTacToe()
    end = False
    while not end:
        end = game.move(gd.generate_random_elem(game))

    return game, game.winner()


if __name__ == "__main__":
    count = 100000
    dic = {}

    for _ in range(count):
        game, res = create_learning_teacher_game()
        dic[tuple(game)] = res

    print(len(dic.keys()))
    fw.save_dict_to_file(dic, "games.txt")