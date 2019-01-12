from time import sleep

from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QFrame, QMessageBox, QLabel
from PyQt5 import uic
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon

from TicTacToe.ElemCourse import ElemCourse
from TicTacToe.TicTacToe import TicTacToe
from players.Computer import Computer
from utils.file_worker import load_dict_from_file


class MainWindow(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        uic.loadUi("game/frame.ui", self)
        self.game_ui = None
        self.ico = "game/ttt.svg"
        self.initUI()

    def initUI(self):
        self.setWindowIcon(QIcon(self.ico))
        self.exit_but.clicked.connect(QCoreApplication.instance().quit)
        self.pve_but.clicked.connect(self.pve_but_clicked)
        self.pvp_but.clicked.connect(self.pvp_but_clicked)

    def set_game_ui(self, game_ui):
        self.game_ui = game_ui

    def pve_but_clicked(self):
        self.hide()
        self.game_ui.pve()

    def pvp_but_clicked(self):
        self.hide()
        self.game_ui.pvp()


class GameWindow(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        uic.loadUi("game/game.ui", self)
        self.radio_buts = [self.pl_first, self.comp_first]
        self.buttons = [self.but_1, self.but_2, self.but_3,
                        self.but_4, self.but_5, self.but_6,
                        self.but_7, self.but_8, self.but_9]
        self.ico = "game/ttt.svg"
        self.initUI()
        self.game = None
        self.comp_turn = None
        self.comp = None

    def initUI(self):
        for but in self.radio_buts:
            but.hide()
        for key, but in enumerate(self.buttons):
            but.clicked.connect(self.player_move(key))
        self.enabled_all(False)
        self.setWindowIcon(QIcon(self.ico))
        self.to_menu_but.clicked.connect(self.to_menu)

    def to_menu(self):
        self.hide()
        self.start_pvp()
        self.main_ui.show()
        self.game = TicTacToe()

    def set_main_ui(self, main_ui):
        self.main_ui = main_ui

    def comp_move(self):
        print("COMP_MOVE")
        self.comp.move()
        print("COMP_MOVE2")
        last_move = self.game[len(self.game) - 1]
        self.buttons[3*last_move.x + last_move.y].setText("o" if self.game.current_turn else "x")
        if self.game.check_end():
            self.end_game()
        else:
            self.status_label.setText(f"{'First' if self.game.current_turn else 'Second'} player's move")

    def player_move(self, key):
        def helper():
            print(key)
            try:
                self.game.add(ElemCourse(key // 3, key % 3))
                print(self.game)
            except AssertionError:
                pass
            else:
                self.buttons[key].setText("o" if self.game.current_turn else "x")
                if self.game.check_end():
                    self.end_game()
                else:
                    self.status_label.setText(f"{'First' if self.game.current_turn else 'Second'} player's move")
                    # sleep(5)
                    if self.comp_turn == 0 or self.comp_turn == 1:  # if defined
                        self.comp_move()

        return helper

    def end_game(self):
        self.enabled_all(False)
        self.start_but.setText("Reset")
        self.start_but.clicked.connect(self.start_prepare)  # here should do start pvp or start pve
        self.start_but.show()

        if self.game.winner() == -1:
            self.status_label.setText("Nobody wins")
        else:
            self.status_label.setText(f"{'Second' if self.game.current_turn else 'First'} player wins!")

    def enabled_all(self, flag):
        for but in self.buttons:
            but.setEnabled(flag)

    def pve(self):
        for but in self.radio_buts:
            but.show()
        self.radio_buts[0].setChecked(True)
        for but in self.buttons:
            but.show()
        self.enabled_all(False)
        self.status_label.setText("")
        self.start_but.setText("Start")
        self.start_but.show()
        self.start_but.clicked.connect(self.start_pve)
        self.comp_turn = None
        self.comp = Computer(load_dict_from_file("student_experience.txt"), self.game)
        self.show()

    def pvp(self):
        for but in self.buttons:
            but.show()
        self.enabled_all(False)
        self.status_label.setText("")
        self.start_but.setText("Start")
        self.start_but.show()
        self.start_but.clicked.connect(self.start_pvp)
        self.show()

    def start_prepare(self):
        for but in self.buttons:
            but.setText("")
        self.start_but.hide()
        self.enabled_all(True)
        self.status_label.setText("First player's move")
        self.game = TicTacToe()

    def start_pvp(self):
        self.start_prepare()

    def start_pve(self):
        self.start_prepare()
        self.comp_turn = 0 if self.radio_buts[0].isChecked() else 1
        for but in self.radio_buts:
            but.hide()

        if self.comp_turn == 1:
            self.comp_move()


class GameGUI(object):

    def __init__(self):
        self.main_ui = MainWindow()
        self.main_ui.show()

        self.game_ui = GameWindow()
        self.game_ui.hide()

        self.game_ui.set_main_ui(self.main_ui)
        self.main_ui.set_game_ui(self.game_ui)
