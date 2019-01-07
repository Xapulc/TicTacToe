import FileWorker as fw
from ElemCourse import ElemCourse
from LearningGame import LearningGame
from TicTacToe import TicTacToe


def create_learning_student_game(teacher_dic, student_dic, start=None):
    """
    :return: moves in the game and result (who winner)
    """
    game = LearningGame(teacher_dic.copy(), student_dic.copy(), start) if not start \
        else LearningGame(teacher_dic.copy(), student_dic.copy(), TicTacToe())
    course_game = game.start(0.5)

    # print(game)
    return course_game, course_game.winner()


if __name__ == "__main__":
    count = 1000
    dic = {}
    teacher_dic = fw.load_dict_from_file("games.txt")
    for i in range(3):
        for j in range(3):
            for k in range(3):
                if k != i:
                    for l in range(3):
                        if l != j:
                            filtered_teacher_dic = teacher_dic.copy()
                            start = TicTacToe([ElemCourse(i, j), ElemCourse(k, l)])
                            start.filter(filtered_teacher_dic)

                            for _ in range(count):
                                game, res = create_learning_student_game(filtered_teacher_dic, dic, start)
                                dic[tuple(game)] = res
                                # print(game)

                            print(f"maked on {100 * (27*i + 9*j + 3*k + l)/81:.0f}%")

    fw.save_dict_to_file(dic, "games2.txt")
    print(len(dic.keys()))
