from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QSizePolicy

import matplotlib
matplotlib.use('Qt5Agg')

import  numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class MyMplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):

        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        self.axes.grid('on')
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def f(self,t):
        return np.exp(-t) * np.cos(2 * np.pi * t)

    def compute_initial_figure(self):
        t1 = np.arange(0.0, 5.0, 0.1)
        t2 = np.arange(0.0, 5.0, 0.02)



        plt.figure(1)
        plt.subplot(211)
        plt.plot(t1, self.f(t1), 'bo', t2, self.f(t2), 'k')

        plt.subplot(212)
        plt.plot(t2, np.cos(2 * np.pi * t2), 'r--')
        plt.show()

from incPage import Ui_Form

import sys

class MainWin(QtWidgets.QMainWindow, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.widget = MyMplCanvas(parent=self)
        self.widget.setGeometry(QtCore.QRect(360, 9, 345, 304))
        self.widget.setObjectName("widget")


    def Pause(self):
        self.Draw()
        pass

    def Draw(self):
        self.widget.compute_initial_figure()
        pass







if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mwin = MainWin()
    mwin.show()
    sys.exit(app.exec_())