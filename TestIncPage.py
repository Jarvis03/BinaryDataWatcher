from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QSizePolicy, QVBoxLayout

import matplotlib
matplotlib.use('Qt5Agg')

import  numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar

from incPage import Ui_MainWindow
from MyWidgets import MyFigure_Inc

import sys

class MainWin(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def Pause(self):
        self.Draw()
        pass



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mwin = MainWin()
    mwin.show()
    sys.exit(app.exec_())