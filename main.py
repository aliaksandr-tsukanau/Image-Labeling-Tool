import sys

from PyQt5.QtWidgets import QApplication

from ui.setup_window import SetupWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SetupWindow()
    ex.show()
    sys.exit(app.exec_())
