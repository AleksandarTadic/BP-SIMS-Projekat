import sys
from PySide2 import QtWidgets, QtGui, QtCore
from gui.main_window import MainWindow
from gui.appearence.appearence import *

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle(QtWidgets.QStyleFactory.create("fusion"))
    set_theme_by_current_time(app)
    window = MainWindow(app)
    window.show()
    sys.exit(app.exec_())
    