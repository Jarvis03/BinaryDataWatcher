import sys
import time

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QSizePolicy, QVBoxLayout, QLineEdit, QMessageBox
from PyQt5.QtCore import QTimer, QThread
from PyQt5.QtGui import QTextDocument


import serial
import serial.tools.list_ports

import  numpy as np

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import matplotlib.dates as matdates


def get_time_stamp(ct):
    local_time = time.localtime(ct)
    data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
    data_secs = (ct - int(ct)) * 1000
    time_stamp = "%s.%03d" % (data_head, data_secs)
    return time_stamp

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
        self.document().setMaximumBlockCount(18000)
        self.appendEnable = True


    def append(self, p_str):
        if self.appendEnable == False:
            return
        if self.document().blockCount() >= 18000:
            self.clear()
        super().append(p_str)

    def setAppendeEnable(self, enable=True):
        self.appendEnable = enable

class MyFigureCanvas(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        plt.rcParams['font.sans-serif'] = ['FangSong']  # 指定默认字体
        plt.rcParams['axes.unicode_minus'] = False

        self.figure = Figure((5.0, 4.0), dpi=100)

        self.canvas = FigureCanvas(self.figure)
        self.canvas.setParent(self)
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.textbox = QLineEdit()
        self.textbox.setMinimumWidth(200)

        vbox = QVBoxLayout(self)
        vbox.addWidget(self.toolbar)
        vbox.addWidget(self.canvas)

    def on_draw(self,ld):
        pass

class MyFigure_Inc(MyFigureCanvas):
    def __init__(self, parent=None):

        super().__init__(parent)

        self.axes = self.figure.add_subplot(111)
        self.axes.grid(True)
        self.axes.set_title("倾斜仪读数显示", fontsize=11)
        self.axes.set_xlabel('时间')
        self.axes.set_ylabel('--')
        self.axes.set_ylim(auto=True)

        # 绘图数据，每小时清零（3600*5）
        self.maxDataLen = 18000
        self.drawData = list()

        self.canvas.draw()

        self.timerDraw = QTimer(self)
        self.timerDraw.timeout.connect(self.on_timer)
        self.timerDraw.start(1000)

    def on_timer(self):
        self.canvas.draw()

    def on_draw(self, ld):
        try:
            if not ld:
                return

            if len(self.drawData) > self.maxDataLen:
                self.drawData.clear()

            for d in ld:
                self.drawData.append(d)

            nd = np.array(self.drawData)

            # # 横轴为时间的处理
            # dates = matdates.epoch2num(nd[:, 0])
            # self.axes.plot_date(dates, nd[:,1],color='r')
            # self.axes.plot_date(dates, nd[:,2], color='g')
            # self.axes.xaxis.set_major_formatter(matdates.DateFormatter('%m%d %H:%M:%S'))
            # self.axes.xaxis.set_tick_params(rotation=30, labelsize=8)

            self.axes.lines.clear()
            self.axes.plot(nd[:,0], nd[:, 1],color='r',label='X 方向倾角')
            self.axes.plot(nd[:,0], nd[:, 2], color='g',label='Y 方向倾角')

            self.axes.set_xlim(left=nd[0, 0], auto=True)
            self.axes.legend(loc='upper left', frameon=True)

        except Exception as err:
            QMessageBox.information(self, "on_draw", str(err), QMessageBox.Ok)

class MyFigure_Imu(MyFigureCanvas):
    finished = QtCore.pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)

        # 绘图数据，每10min清零（60000）
        self.maxDataLen = 18000
        self.drawData = list()

        self .axList = list()
        title = ['gyro_dx', 'gyro_dy', 'gyro_dz', 'acc_dx', 'acc_dy', 'acc_dz']
        self.figure.set_constrained_layout(True)
        self.figure.set_constrained_layout_pads(w_pad=0.4, h_pad=0.2, hspace=0.1, wspace=0.05)
        for a in range(6):
            ax = self.figure.add_subplot(2, 3, a+1)

            ax.grid(True)
            ax.set_title(title[a], fontsize=11)
            ax.set_xlabel('帧计数')
            ax.set_ylabel('器件读数（标注单位）')
            ax.set_ylim(auto=True)
            self.axList.append(ax)

        self.canvas.draw()

        self.timerDraw = QTimer(self)
        self.timerDraw.timeout.connect(self.on_timer)
        self.timerDraw.start(1000)

    def on_timer(self):
        self.canvas.draw()

    def on_draw(self, ld):
        if not ld:
            return

        try:
            if len(self.drawData) > self.maxDataLen:
                self.drawData.clear()

            for d in ld:
                self.drawData.append(d)

            nd = np.array(self.drawData)

            for i in range(len(self.axList)):
                if i<3:
                    color = 'r'
                else:
                    color = 'g'

                self.axList[i].lines.clear()
                self.axList[i].plot(nd[:, 1], nd[:, i+2], color=color)
                self.axList[i].set_xlim(left=nd[0, 1], auto=True)

        except Exception as err:
            QMessageBox.information(self, "on_draw", str(err), QMessageBox.Ok)


    def reset_draw(self):
        self.timerDraw.stop()

        self.drawData.clear()

        for i in range(len(self.axList)):
            self.axList[i].lines.clear()

        self.canvas.draw()

        self.timerDraw.start(1000)
