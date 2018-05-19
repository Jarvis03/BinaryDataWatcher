import sys

from PyQt5 import QtCore, QtGui, QtWidgets

import serial
import serial.tools.list_ports

import matplotlib
from PyQt5.QtWidgets import QSizePolicy, QVBoxLayout, QLineEdit

matplotlib.use('Qt5Agg')

import  numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import time


def get_time_stamp(ct):
    local_time = time.localtime(ct)
    data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
    data_secs = (ct - int(ct)) * 1000
    time_stamp = "%s.%03d" % (data_head, data_secs)

    return time_stamp

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

    def myDraw(self,ld):
        pass

class MyFigure_Inc(MyFigureCanvas):
    def __init__(self, parent=None):
        self.x = list()
        self.y = list()
        self.t = list()

        super().__init__(parent)
        self.axes = self.figure.add_subplot(111)
        self.axes.grid(True)
        self.axes.set_title("倾斜仪读数显示", fontsize=11)

    def myDraw(self, ld):
        self.axes.clear()
        for d in ld:
            self.x.append(d[1])
            self.y.append(d[2])
            self.t.append(int(d[0]))
            break
        if len(self.t) > 3600:
            del self.x[0]
            del self.y[0]
            del self.t[0]

        self.line_x = self.axes.plot(self.t, self.x, label='X 方向倾角', color='r')
        self.line_y = self.axes.plot(self.t, self.y, label='Y 方向倾角', color='g')

        self.axes.legend(loc='best', fontsize=9)
        self.canvas.draw()

class MyFigure_Imu(MyFigureCanvas):
    def __init__(self, parent=None):
        super().__init__(parent)

        self .axList = list()
        title = ['gyro_dx', 'gyro_dy', 'gyro_dz', 'acc_dx', 'acc_dy', 'acc_dz']
        for a in range(6):
            ax = self.figure.add_subplot(2,3,a+1)
            ax.grid(True)
            ax.set_title(title[a], fontsize=11)
            self.axList.append(ax)

    def myDraw(self, ld):
        pass

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
    sinOnDraw = QtCore.pyqtSignal(list)

    def __init__(self,parent=None):
        super().__init__(parent)

        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        self.textEdit = QTextEdit_AppendEnable(self)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.textEdit.setFont(font)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout.addWidget(self.textEdit, 0, 0, 1, 2)
        self.btn_clear = QtWidgets.QPushButton(self)
        self.btn_clear.setObjectName("btn_clear")
        self.gridLayout.addWidget(self.btn_clear, 1, 1, 2, 1)
        self.btn_stop = QtWidgets.QPushButton(self)
        self.btn_stop.setCheckable(True)
        self.btn_stop.setChecked(False)
        self.btn_stop.setObjectName("btn_stop")
        self.gridLayout.addWidget(self.btn_stop, 2, 0, 1, 1)
        self.widget = MyFigure_Inc(self)
        self.widget.setObjectName("widget")
        self.gridLayout.addWidget(self.widget, 0, 2, 3, 1)
        self.gridLayout.setColumnMinimumWidth(0, 160)
        self.gridLayout.setColumnMinimumWidth(1, 160)
        self.gridLayout.setColumnMinimumWidth(2, 480)

        self.btn_stop.setText("暂停")
        self.btn_clear.setText("清空")

        self.btn_stop.clicked['bool'].connect(self.Pause)
        self.btn_clear.clicked.connect(self.textEdit.clear)
        self.sinOnDraw[list].connect(self.widget.myDraw)

    def Pause(self,pressed):
        if pressed:
            self.btn_stop.setText('继续')
            self.textEdit.setAppendeEnable(False)
        else:
            self.btn_stop.setText('暂停')
            self.textEdit.setAppendeEnable(True)

    def Refresh(self, ld):
        for d in ld:
            ts = get_time_stamp(d[0])
            self.textEdit.append(ts + ": "+ str(d[1:]))
        self.sinOnDraw.emit(ld)

class tabPage_Imu(QtWidgets.QWidget):

    def __init__(self,parent=None):
        super().__init__(parent)

        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tableWidget = QtWidgets.QTableWidget(self)
        self.tableWidget.setShowGrid(True)
        self.tableWidget.setGridStyle(QtCore.Qt.DotLine)
        self.tableWidget.setWordWrap(True)
        self.tableWidget.setCornerButtonEnabled(True)
        self.tableWidget.setRowCount(600)
        self.tableWidget.setColumnCount(13)
        self.tableWidget.setObjectName("tableWidget")
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(11, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(12, item)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(60)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(60)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setDefaultSectionSize(16)
        self.tableWidget.verticalHeader().setMinimumSectionSize(16)
        self.verticalLayout_2.addWidget(self.tableWidget)
        self.widget = MyFigure_Imu(self)
        self.widget.setObjectName("widget")
        self.tableWidget.raise_()
        self.verticalLayout_2.addWidget(self.widget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_starttime = QtWidgets.QLabel(self)
        self.label_starttime.setObjectName("label_starttime")
        self.horizontalLayout.addWidget(self.label_starttime)
        self.label_duration = QtWidgets.QLabel(self)
        self.label_duration.setObjectName("label_duration")
        self.horizontalLayout.addWidget(self.label_duration)
        self.label_frameCount = QtWidgets.QLabel(self)
        self.label_frameCount.setObjectName("label_frameCount")
        self.horizontalLayout.addWidget(self.label_frameCount)
        self.btn_reset = QtWidgets.QPushButton(self)
        self.btn_reset.setObjectName("btn_reset")
        self.horizontalLayout.addWidget(self.btn_reset)
        self.horizontalLayout.setStretch(0, 4)
        self.horizontalLayout.setStretch(1, 2)
        self.horizontalLayout.setStretch(2, 2)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout_2.setStretch(1, 3)
        self.tableWidget.raise_()
        self.btn_reset.raise_()
        self.widget.raise_()

        item = self.tableWidget.verticalHeaderItem(0)
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText("frameID")
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText( "gyro_dx")
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText( "gyro_dy")
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText( "gyro_zx")
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText( "acc_dx")
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText( "acc_dy")
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText( "acc_dz")
        item = self.tableWidget.horizontalHeaderItem(7)
        item.setText( "gyro_tx")
        item = self.tableWidget.horizontalHeaderItem(8)
        item.setText( "gyro_ty")
        item = self.tableWidget.horizontalHeaderItem(9)
        item.setText( "gyro_tz")
        item = self.tableWidget.horizontalHeaderItem(10)
        item.setText( "acc_tx")
        item = self.tableWidget.horizontalHeaderItem(11)
        item.setText( "acc_ty")
        item = self.tableWidget.horizontalHeaderItem(12)
        item.setText( "acc_tz")
        self.label_starttime.setText( "端口启动时间：")
        self.label_duration.setText( "运行时长：")
        self.label_frameCount.setText( "接收数据总帧数")
        self.btn_reset.setText( "复位")

        self.btn_reset.clicked.connect(self.BtnResetTime)


    def BtnResetTime(self):
        pass

    def Refresh(self, ld):
        pass