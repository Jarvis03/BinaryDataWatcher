import sys

from PyQt5 import QtCore, QtGui, QtWidgets

import serial
import serial.tools.list_ports

import matplotlib
from PyQt5.QtWidgets import QSizePolicy

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

        # t1 = np.arange(0.0, 5.0, 0.1)
        # t2 = np.arange(0.0, 5.0, 0.02)
        #
        # self.axes2.plot(t1, self.f(t1), 'bo', t2, self.f(t2), 'k')
        # self.axes.plot(t2, np.cos(2 * np.pi * t2), 'r--')



# import matplotlib
# matplotlib.use('Qt5Agg')
# # 使用 matplotlib中的FigureCanvas (在使用 Qt5 Backends中 FigureCanvas继承自QtWidgets.QWidget)
# from matplotlib.figure import Figure
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
#
# class Figure_Canvas(FigureCanvas):   # 通过继承FigureCanvas类，使得该类既是一个PyQt5的Qwidget，又是一个matplotlib的FigureCanvas，这是连接pyqt5与matplot                                          lib的关键
#
#     def __init__(self, parent=None, width=11, height=5, dpi=100):
#         fig = Figure(figsize=(width, height), dpi=100)  # 创建一个Figure，注意：该Figure为matplotlib下的figure，不是matplotlib.pyplot下面的figure
#
#         FigureCanvas.__init__(self, fig) # 初始化父类
#         self.setParent(parent)
#
#         self.axes = fig.add_subplot(111) # 调用figure下面的add_subplot方法，类似于matplotlib.pyplot下面的subplot方法
#
#     def test(self):
#         x = [1,2,3,4,5,6,7,8,9]
#         y = [23,21,32,13,3,132,13,3,1]
#         self.axes.plot(x, y)


class QComboBox_SelSerialNum(QtWidgets.QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)

    def showPopup(self):
        Com_List = []
        port_list = list(serial.tools.list_ports.comports())
        self.clear()
        self.addItem("None")
        for port in port_list:
            Com_List.append(port[0])
            self.addItem(port[0])

        super().showPopup()

class QTextEdit_AppendEnable(QtWidgets.QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.appendEnable = True

    def append(self, p_str):
        if self.appendEnable == False:
            return
        super().append(p_str)

    def setAppendeEnable(self, enable=True):
        self.appendEnable = enable



class tabPage_Inclinometer(QtWidgets.QWidget):
    def __init__(self,prent=None):
        super().__init__(prent)

        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.textEdit = QTextEdit_AppendEnable(self)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.textEdit.setFont(font)
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setReadOnly(True)
        self.gridLayout.addWidget(self.textEdit, 0, 0, 1, 2)
        self.btn_clear = QtWidgets.QPushButton(self)
        self.btn_clear.setObjectName("btn_clear")
        self.gridLayout.addWidget(self.btn_clear, 1, 1, 1, 1)
        self.btn_stop = QtWidgets.QPushButton(self)
        self.btn_stop.setObjectName("btn_stop")
        self.btn_stop.setCheckable(True)
        self.btn_stop.setChecked(False)
        self.gridLayout.addWidget(self.btn_stop, 1, 0, 1, 1)
        self.gridLayout.setColumnMinimumWidth(0, 180)
        self.gridLayout.setColumnMinimumWidth(1, 180)
        self.horizontalLayout.addLayout(self.gridLayout)
        self.gphwidge = QtWidgets.QWidget()
        self.gphwidge.setObjectName("graphicsView")
        self.horizontalLayout.addWidget(self.gphwidge)

        self.btn_stop.setText("暂停")
        self.btn_clear.setText("清空")

        self.btn_stop.clicked['bool'].connect(self.Pause)
        self.btn_clear.clicked.connect(self.textEdit.clear)

        # dr = Figure_Canvas()
        # # 实例化一个FigureCanvas
        # dr.test()  # 画图
        # graphicscene = QtWidgets.QGraphicsScene()  # 第三步，创建一个QGraphicsScene，因为加载的图形（FigureCanvas）不能直接放到graphicview控件中，必须先放到graphicScene，然后再把graphicscene放到graphicview中
        # graphicscene.addWidget(dr)  # 第四步，把图形放到QGraphicsScene中，注意：图形是作为一个QWidget放到QGraphicsScene中的
        # self.graphicsView.setScene(graphicscene)  # 第五步，把QGraphicsScene放入QGraphicsView
        # self.graphicsView.show()  # 最后，调用show方法呈现图形！Voila!!
        # #self.setCentralWidget(self.graphicview)
        # #self.graphicsView.setFixedSize(800, 600)

    def Pause(self,pressed):
        if pressed:
            self.btn_stop.setText('继续')
            self.textEdit.setAppendeEnable(False)
        else:
            self.btn_stop.setText('暂停')
            self.textEdit.setAppendeEnable(True)


class tabPage_Imu(QtWidgets.QWidget):
    def __init__(self,prent=None):
        super().__init__(prent)
        pass
