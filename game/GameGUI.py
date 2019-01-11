from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QFrame, QMessageBox, QLabel
from PyQt5 import uic
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon

from TicTacToe.ElemCourse import ElemCourse
from TicTacToe.TicTacToe import TicTacToe


class MainWindow(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        uic.loadUi("frame.ui", self)
        self.game_ui = None
        self.ico = "ttt.svg"
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
        uic.loadUi("game.ui", self)
        self.radio_buts = [self.pl_first, self.comp_first]
        self.buttons = [self.but_1, self.but_2, self.but_3,
                        self.but_4, self.but_5, self.but_6,
                        self.but_7, self.but_8, self.but_9]
        self.ico = "ttt.svg"
        self.initUI()
        self.game = None

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
        self.reset_game()
        self.main_ui.show()
        self.game = TicTacToe()

    def set_main_ui(self, main_ui):
        self.main_ui = main_ui

    def player_move(self, key):
        def helper():
            try:
                self.game.add(ElemCourse(key // 3, key % 3))
            except AssertionError:
                pass
            else:
                self.buttons[key].setText("x" if self.game.current_turn() else "o")
                if self.game.check_end():
                    self.end_game()
                else:
                    self.status_label.setText(f"{'First' if self.game.current_turn() else 'Second'} player's move")

        return helper

    def end_game(self):
        self.enabled_all(False)
        self.start_but.setText("Reset")
        self.start_but.clicked.connect(self.start_pvp())
        self.start_but.show()

        if self.game.winner() == -1:
            self.status_label.setText("Nobody wins")
        else:
            self.status_label.setText(f"{'First' if self.game.current_turn() else 'Second'} player wins!")

    def enabled_all(self, flag):
        for but in self.buttons:
            but.setEnabled(flag)

    def pve(self):
        for but in self.radio_buts:
            but.show()
        self.radio_buts[0].setChecked(True)
        for but in self.buttons:
            but.show()
        self.start_but.clicked.connect(self.start_pve)
        self.enabled_all(False)
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

    def start_pvp(self):
        for but in self.buttons:
            but.setText("")
        self.start_but.hide()
        self.enabled_all(True)
        self.status_label.setText("First player's move")
        self.game = TicTacToe()

    def start_pve(self):
        self.start_but.hide()
        self.start_but.setText("Reset")
        self.start_but.clicked.connect(self.reset_game)
        for but in self.radio_buts:
            but.hide()


class GameGUI(object):

    def __init__(self):
        self.main_ui = MainWindow()
        self.main_ui.show()

        self.game_ui = GameWindow()
        self.game_ui.hide()

        self.game_ui.set_main_ui(self.main_ui)
        self.main_ui.set_game_ui(self.game_ui)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = GameGUI()
    sys.exit(app.exec_())
