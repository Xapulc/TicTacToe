from utils.file_worker import save_dict_to_file, load_dict_from_file
from TicTacToe.ElemCourse import ElemCourse
from learning.LearningGame import LearningGame
from TicTacToe.TicTacToe import TicTacToe


def create_learning_student_game(teacher_dic, student_dic, probability_random_move, beginning_game=None):
    """
    :param teacher_dic: teacher's experience
    :param student_dic: student's experience
    :param probability_random_move: this is parameter of random move
    :param beginning_game: previous game, if none -> start new game
    :return: moves in the game and result (who winner)
    """
    game = LearningGame(teacher_dic.copy(), student_dic.copy(), beginning_game) if not beginning_game \
        else LearningGame(teacher_dic.copy(), student_dic.copy())
    course_game, is_student_win = game.start(probability_random_move)
    return course_game, course_game.winner(), is_student_win


def filter_data(beginning_game, dic):
    """
    filters the dictionary, removing scripts that are not suitable for this game
    :param beginning_game: current state of game
    :param dic: filterable dictionary
    :return:
    """
    if len(beginning_game) > 0:
        keys = set(dic.keys())
        for key in keys:
            if key[:len(beginning_game)] != tuple(beginning_game):
                dic.pop(key)


def learn_student(count, probability_random_move):
    """
    :param count: number of games to be played by student with teacher (will be played 72 * count games)
    :param probability_random_move: this is parameter of random move
    This is script code for teaching student experience-based teacher
    """
    student_wins = 0
    teacher_wins = 0
    student_experience_path = "student_experience.txt"
    teacher_experience_path = "teacher_experience.txt"
    student_dic = load_dict_from_file(student_experience_path)
    teacher_dic = load_dict_from_file(teacher_experience_path)
    for i in range(3):
        for j in range(3):
            for k in range(3):
                for l in range(3):
                    if not (l == j and k == i):
                        filtered_teacher_dic = teacher_dic.copy()
                        filtered_student_dic = student_dic.copy()
                        beginning_game = TicTacToe([ElemCourse(i, j), ElemCourse(k, l)])
                        filter_data(beginning_game, filtered_teacher_dic)
                        filter_data(beginning_game, filtered_student_dic)
                        for _ in range(count):
                            game, res, is_student_win = create_learning_student_game(filtered_teacher_dic,
                                                                                     filtered_student_dic,
                                                                                     probability_random_move,
                                                                                     beginning_game)
                            student_wins += (1 if is_student_win == 1 else 0)
                            teacher_wins += (1 if is_student_win == -1 else 0)
                            student_dic[tuple(game)] = res
                        print(f"complete on {100 * (27 * i + 9 * j + 3 * k + l) / 81:.0f}%")

    print(f"Student has {100 * (student_wins / (72 * count)):.2f}% wins")
    print(f"Teacher has {100 * (teacher_wins / (72 * count)):.2f}% wins")
    save_dict_to_file(student_dic, student_experience_path)
    print(len(student_dic.keys()))
