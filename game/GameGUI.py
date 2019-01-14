from PyQt5.QtWidgets import QWidget, QPushButton
from PyQt5 import uic
from PyQt5.QtCore import QCoreApplication, QSize
from PyQt5.QtGui import QIcon

from TicTacToe.ElemCourse import ElemCourse
from TicTacToe.TicTacToe import TicTacToe
from players.Computer import Computer
from utils.file_worker import load_dict_from_file, save_dict_to_file


class MainWindow(QWidget):
    """
    Class is responsible for window with main menu
    """

    def __init__(self):
        QWidget.__init__(self)
        self.game_ui = None
        self.ico = "game/ttt.svg"
        self.initUI()

    def initUI(self):
        """
        Initialisation GUI and connecting buttons with functions
        """
        uic.loadUi("game/frame.ui", self)
        self.setWindowIcon(QIcon(self.ico))
        self.exit_but.clicked.connect(QCoreApplication.instance().quit)
        self.pve_but.clicked.connect(self.mode_game_but_clicked("pve"))
        self.pvp_but.clicked.connect(self.mode_game_but_clicked("pvp"))

    def set_game_ui(self, game_ui):
        """
        This need for connection with game UI and main menu UI
        :param game_ui: GameWindow class instance
        """
        self.game_ui = game_ui

    def mode_game_but_clicked(self, mode):
        """
        :param mode: pvp or pve
        :return: an function which, at the press of a button, prepares the window for the corresponding game mode
        """

        def helper():
            self.hide()
            self.game_ui.draws_num = 0
            self.game_ui.player1_win_num = 0
            self.game_ui.player2_win_num = 0
            self.game_ui.pve_window_prepare() if mode == "pve" else self.game_ui.pvp_window_prepare()

        return helper


class GameWindow(QWidget):
    """
    Class is responsible for window with game
    Contains playing field, start/reset, to main menu, hint and radio buttons
    """

    def __init__(self):
        QWidget.__init__(self)
        uic.loadUi("game/game.ui", self)
        self.radio_buts = [self.pl_first, self.comp_first]
        self.buttons = [self.but_1, self.but_2, self.but_3,
                        self.but_4, self.but_5, self.but_6,
                        self.but_7, self.but_8, self.but_9]
        self.ico = "game/ttt.svg"
        self.hint_but_ico = "game/hint_but_ico.svg"
        self.game = None
        self.pvp_window_prepare = self.game_window_prepare("pvp")
        self.pve_window_prepare = self.game_window_prepare("pve")
        self.draws_num = 0
        self.player1_wins_num = 0
        self.player2_wins_num = 0
        self.comp_turn = None
        self.comp = None
        self.last_hint_num = None
        self.experience_path = "old_student_experience"
        self.cross_ico = QIcon("game/cross.svg")
        self.circle_ico = QIcon("game/circle.svg")
        self.hint_ico = QIcon("game/lamp.svg")
        self.none_ico = QIcon(None)
        self.initUI()

    def initUI(self):
        """
        Initialisation GUI and connecting buttons with functions
        """
        for but in self.radio_buts:
            but.hide()
        for key, but in enumerate(self.buttons):
            but.clicked.connect(self.player_move(key))
        self.enabled_all(False)
        self.setWindowIcon(QIcon(self.ico))
        self.to_menu_but.clicked.connect(self.to_menu)
        self.hint_but.clicked.connect(self.hint)
        self.hint_but.setIcon(QIcon(self.hint_but_ico))
        self.hint_but.setIconSize(QSize(40, 40))

    def hint(self):
        """
        Computer calculates more effective move and set in cell "!"
        """
        el = self.comp.hint_move()
        self.last_hint_num = 3 * el.x + el.y
        self.buttons[self.last_hint_num].setIcon(self.hint_ico)

    def to_menu(self):
        """
        Function for to_menu_but
        """
        self.hide()
        self.game_start()
        self.main_ui.show()
        self.game = TicTacToe()

    def set_main_ui(self, main_ui):
        """
        This need for connection with game UI and main menu UI
        :param main_ui: MainWindow class instance
        """
        self.main_ui = main_ui

    def comp_move(self):
        """
        Make computer move in this game and checking end
        """
        self.comp.move()
        last_move = self.game[len(self.game) - 1]
        self.buttons[3 * last_move.x + last_move.y].setIcon(self.circle_ico if self.game.current_turn else self.cross_ico)
        if self.game.check_end():
            self.end_game()
        else:
            self.status_label.setText("Player's move")

    def player_move(self, key):
        """
        :param key: number of button
        :return: an function which, at the press of a button, set in cell O or X
        """
        def helper():
            try:
                self.game.add(ElemCourse(key // 3, key % 3))
            except AssertionError:
                pass
            else:
                if self.last_hint_num is not None:
                    self.buttons[self.last_hint_num].setIcon(self.none_ico)
                    self.last_hint_num = None
                self.buttons[key].setIcon(self.circle_ico if self.game.current_turn else self.cross_ico)
                if self.game.check_end():
                    self.end_game()
                else:
                    if self.comp_turn is not None:
                        self.status_label.setText(f"Computer's move")
                        self.comp_move()
                    else:
                        self.status_label.setText(f"{'First' if self.game.current_turn else 'Second'} player's move")

        return helper

    def statistic(self):
        if self.game.winner() == -1:
            self.draws_num += 1
            if self.comp_turn is None:
                return "Nobody wins\n" \
                      + f"First player's wins: {self.player1_wins_num}\n" \
                      + f"Second player's wins: {self.player2_wins_num}\n" \
                      + f"Draws: {self.draws_num}"
            else:
                return "Nobody wins\n" \
                      + f"Player's wins: {self.player1_wins_num}\n" \
                      + f"Computer's wins: {self.player2_wins_num}\n" \
                      + f"Draws: {self.draws_num}"

        else:
            if self.comp_turn is None:
                self.player1_wins_num += self.game.current_turn
                self.player2_wins_num += 1 - self.game.current_turn
                return f"{'Second' if self.game.current_turn else 'First'} player wins!\n" \
                       + f"First player's wins: {self.player1_wins_num}\n" \
                       + f"Second player's wins: {self.player2_wins_num}\n" \
                       + f"Draws: {self.draws_num}"
            else:
                if self.comp_turn == self.game.winner():
                    self.player2_wins_num += 1
                else:
                    self.player1_wins_num += 1
                return f"{'Computer' if self.comp_turn == self.game.winner() else 'Player'} wins!\n" \
                       + f"Player's wins: {self.player1_wins_num}\n" \
                       + f"Computer's wins: {self.player2_wins_num}\n" \
                       + f"Draws: {self.draws_num}"

    def end_game(self):
        """
        Final actions at the end of the game
        """
        self.enabled_all(False)
        self.start_res_but.setText("Reset")
        self.start_res_but.show()
        self.hint_but.hide()
        if self.comp_turn is None:
            self.start_res_but.clicked.disconnect(self.pvp_start)
            self.start_res_but.clicked.connect(self.pvp_window_prepare)
        else:
            self.start_res_but.clicked.disconnect(self.pve_start)
            self.start_res_but.clicked.connect(self.pve_window_prepare)

        self.status_label.setText(self.statistic())

        if self.comp_turn is not None:
            n = self.game[0].x*3 + self.game[0].y
            data = load_dict_from_file(f"{self.experience_path}{n}.txt")
            data[tuple(self.game)] = self.game.winner()
            save_dict_to_file(data, f"{self.experience_path}{n}.txt")

    def enabled_all(self, flag):
        """
        makes all buttons responsible for the game [un]available for pressing
        :param flag: True (enabled) or False (disabled)
        """
        for but in self.buttons:
            but.setEnabled(flag)

    def game_window_prepare(self, mode):
        """
        :param mode: pvp or pve
        :return: an function which, at the press of a button, prepare game for pve or pvp
        """

        def helper():
            for but in self.buttons:
                but.setIcon(self.none_ico)
                but.show()

            for but in self.radio_buts:
                but.show() if mode == "pve" else but.hide()
            self.radio_buts[0].setChecked(True)

            self.enabled_all(False)
            self.status_label.setText("")

            self.start_res_but.setText("Start")
            try:
                self.start_res_but.clicked.disconnect(self.pvp_window_prepare)
            except TypeError:
                pass
            try:
                self.start_res_but.clicked.disconnect(self.pve_window_prepare)
            except TypeError:
                pass
            self.start_res_but.clicked.connect(self.pve_start if mode == "pve" else self.pvp_start)
            self.start_res_but.show()
            self.hint_but.hide()

            self.comp_turn = None
            self.show()

        return helper

    def resizeEvent(self, QResizeEvent):
        super().resizeEvent(QResizeEvent)
        for but in self.buttons:
            but.setIconSize(QSize(0.9*but.width(), 0.9*but.height()))

    def game_start(self):
        """
        help function, same actions for pve and pvp
        """
        self.start_res_but.hide()
        self.hint_but.show()
        self.enabled_all(True)
        self.game = TicTacToe()
        self.comp = Computer(load_dict_from_file("student_experience.txt"), self.game)

    def pvp_start(self):
        """
        function for start button in pvp game
        """
        self.game_start()
        self.comp_turn = None
        self.status_label.setText("First player's move")

    def pve_start(self):
        """
        function for start button in pve game
        """
        self.game_start()
        self.comp_turn = 0 if self.radio_buts[0].isChecked() else 1
        for but in self.radio_buts:
            but.hide()

        if self.comp_turn == 1:
            self.status_label.setText("Computer's move")
            self.comp_move()
        else:
            self.status_label.setText("Player's move")


class GameGUI(object):
    """
    Help class for connecting MainWindow and GameWindow together
    """

    def __init__(self):
        self.main_ui = MainWindow()
        self.main_ui.show()

        self.game_ui = GameWindow()
        self.game_ui.hide()

        self.game_ui.set_main_ui(self.main_ui)
        self.main_ui.set_game_ui(self.game_ui)
