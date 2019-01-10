from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QFrame, QMessageBox, QLabel
from PyQt5 import uic
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon

from game.PlayerGame import PlayerGame


class MainWindow(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        uic.loadUi("frame.ui", self)
        self.game_ui = None
        self.initUI()

    def initUI(self):
        self.setWindowIcon(QIcon("icon.png"))
        self.exit_but.clicked.connect(QCoreApplication.instance().quit)
        self.pve_but.clicked.connect(self.pve_but_clicked)

    def set_game_ui(self, game_ui):
        self.game_ui = game_ui

    def pve_but_clicked(self):
        self.hide()
        self.game_ui.pve()


class GameWindow(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        uic.loadUi("game.ui", self)
        self.initUI()

    def initUI(self):
        self.buttons = [self.but_1, self.but_2, self.but_3,
                        self.but_4, self.but_5, self.but_6,
                        self.but_7, self.but_8, self.but_9]
        self.radio_buts = [self.pl_first, self.comp_first]
        for but in self.radio_buts:
            but.hide()
        for but in self.buttons:
            but.setDisabled(True)
            but.hide()
        self.setWindowIcon(QIcon("icon.png"))
        self.to_menu_but.clicked.connect(self.to_menu)
        self.start_but.clicked.connect(self.startPvE)

    def set_main_ui(self, main_ui):
        self.main_ui = main_ui

    def to_menu(self):
        self.hide()
        self.main_ui.show()

    def pve(self):
        for but in self.radio_buts:
            but.show()
        self.radio_buts[0].setChecked(True)
        for but in self.buttons:
            but.show()
        self.show()

    def startPvE(self):
        self.start_but.hide()
        game = PlayerGame()
        for but in self.radio_buts:
            but.hide()
        game.startWithGUI(self)


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
