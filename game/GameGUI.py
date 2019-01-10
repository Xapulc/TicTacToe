from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QFrame, QMessageBox
from PyQt5 import uic
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon


class MainWindow(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        uic.loadUi("frame.ui", self)
        self.game_ui = None
        self.initUI()

    def initUI(self):
        self.setWindowIcon(QIcon("icon.png"))
        self.exit_but.clicked.connect(QCoreApplication.instance().quit)
        self.pvp_but.clicked.connect(self.pvp_but_clicked)

    def set_game_ui(self, game_ui):
        self.game_ui = game_ui

    def pvp_but_clicked(self):
        self.hide()
        self.game_ui.pvp()


class GameWindow(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        uic.loadUi("game.ui", self)
        self.initUI()

    def initUI(self):
        self.buttons = [self.but_1, self.but_2, self.but_3,
                        self.but_4, self.but_5, self.but_6,
                        self.but_7, self.but_8, self.but_9]
        self.radio_buts = [self.comp_first, self.pl_first]
        for but in self.radio_buts:
            but.hide()
        for but in self.buttons:
            but.setDisabled(True)
            but.hide()
        self.setWindowIcon(QIcon("icon.png"))
        self.to_menu_but.clicked.connect(self.to_menu)

    def set_main_ui(self, main_ui):
        self.main_ui = main_ui

    def to_menu(self):
        self.hide()
        self.main_ui.show()

    def pvp(self):
        p = QPushButton()
        for but in self.radio_buts:
            but.show()
            # but.setEnabled(True)
        self.radio_buts[0].setChecked(True)
        self.show()
        # p.set


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
    # window.show()
    sys.exit(app.exec_())
