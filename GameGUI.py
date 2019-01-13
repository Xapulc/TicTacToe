from PyQt5.QtWidgets import QApplication
from game.GameGUI import GameGUI

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = GameGUI()
    sys.exit(app.exec_())
