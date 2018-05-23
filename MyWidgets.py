import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QSizePolicy, QVBoxLayout, QLineEdit, QMessageBox
from PyQt5.QtCore import QTimer, QThread

import serial
import serial.tools.list_ports

import matplotlib
matplotlib.use('Qt5Agg')

import  numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.animation import FuncAnimation
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


import time


def get_time_stamp(ct):
    local_time = time.localtime(ct)
    data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
    data_secs = (ct - int(ct)) * 1000
    time_stamp = "%s.%03d" % (data_head, data_secs)
    return time_stamp

class DrawPlotThread(QThread):

    def __init__(self, rest, parent=None):
        super().__init__(parent)
        self._rest = rest

    def run(self):
        pass

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
    finished = QtCore.pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)

        self.xleft = 0

        # self.luserList = list()
        # self.bgList = list()

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

            ax.set_autoscale_on(True)
            self.axList.append(ax)

        self.canvas.draw()

        # for ax in self.axList:
        #     self.bgList.append(self.canvas.copy_from_bbox(ax.bbox))

        self.timerC = QTimer(self)
        self.timerC.timeout.connect(self.TimerDraw)
        self.timerC.start(1000)

    def TimerDraw(self):
        self.canvas.draw()
        pass

    def myDraw(self, ld):
        try:
            if not ld:
                return
            # if ld[-1][1] > self.xleft+600:
            #     self.xleft = ld[-1][1]
            #     for ax in self.axList:
            #         ax.set_xlim(self.xleft, self.xleft+600)

            nd = np.array(ld)

            for i in range(len(self.axList)):
                if i<3:
                    color = 'b'
                else:
                    color = 'g'

                # self.canvas.restore_region(self.bgList[i])
                # if not self.axList[i].lines:
                #     self.axList[i].plot(nd[:, 1], nd[:, i + 2], color=color)
                # else:
                #     self.axList[i].lines[0].set_data(nd[:, 1], nd[:, i+2])
                # self.axList[i].draw_artist(self.axList[i].lines[0])
                #
                # self.canvas.blit(self.axList[i].bbox)
                #
                # self.axList[i].set_xlim(self.xleft, self.xleft + 600)

                while self.axList[i].lines:
                    del self.axList[i].lines[0]
                self.axList[i].plot(nd[:, 1], nd[:, i+2], color=color)
                #self.axList[i].draw_artist(self.axList[i].lines[0])

                # bom,top = self.axList[i].get_ylim()
                # vline = self.axList[i].vlines(nd[-1,1], bom, nd[-1,i+2], linestyles='dotted', color='r')
                # self.axList[i].add_line(vline)
            #self.canvas.draw()
        except Exception as err:
            QMessageBox.information(self, "PorcessInclinometer", str(err), QMessageBox.Ok)

    def resetFigure(self):
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
    sinOnDraw = QtCore.pyqtSignal(list)


    def __init__(self,parent=None):
        super().__init__(parent)

        self.tableRowCount = 300
        self.tableColCount = 14

        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.tableWidget = QtWidgets.QTableWidget(self)
        self.tableWidget.setMinimumSize(QtCore.QSize(300, 220))
        self.tableWidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setShowGrid(True)
        self.tableWidget.setGridStyle(QtCore.Qt.DotLine)
        self.tableWidget.setWordWrap(True)
        self.tableWidget.setCornerButtonEnabled(True)
        self.tableWidget.setRowCount(self.tableRowCount)
        self.tableWidget.setColumnCount(self.tableColCount)
        self.tableWidget.setObjectName("tableWidget")

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
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(13, item)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(70)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(70)
        self.tableWidget.verticalHeader().setVisible(True)
        self.tableWidget.verticalHeader().setDefaultSectionSize(17)
        self.tableWidget.verticalHeader().setMinimumSectionSize(17)
        self.horizontalLayout_2.addWidget(self.tableWidget)

        self.tableWidget_2 = QtWidgets.QTableWidget(self)
        self.tableWidget_2.setMinimumSize(QtCore.QSize(300, 220))
        self.tableWidget_2.setMaximumSize(QtCore.QSize(580, 16777215))
        self.tableWidget_2.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget_2.setShowGrid(True)
        self.tableWidget_2.setGridStyle(QtCore.Qt.DotLine)
        self.tableWidget_2.setWordWrap(True)
        self.tableWidget_2.setCornerButtonEnabled(True)
        self.tableWidget_2.setRowCount(7)
        self.tableWidget_2.setColumnCount(7)
        self.tableWidget_2.setObjectName("tableWidget_2")
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(6, item)
        self.tableWidget_2.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget_2.horizontalHeader().setDefaultSectionSize(70)
        self.tableWidget_2.horizontalHeader().setMinimumSectionSize(70)
        self.tableWidget_2.verticalHeader().setVisible(True)
        self.tableWidget_2.verticalHeader().setDefaultSectionSize(25)
        self.tableWidget_2.verticalHeader().setMinimumSectionSize(25)
        self.horizontalLayout_2.addWidget(self.tableWidget_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.widget = MyFigure_Imu(self)
        self.widget.setObjectName("widget")
        self.tableWidget.raise_()
        self.verticalLayout.addWidget(self.widget)

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
        self.btn_Pause = QtWidgets.QPushButton(self)
        self.btn_Pause.setCheckable(True)
        self.btn_Pause.setObjectName("btn_Pause")
        self.horizontalLayout.addWidget(self.btn_Pause)
        self.btn_reset = QtWidgets.QPushButton(self)
        self.btn_reset.setObjectName("btn_reset")
        self.horizontalLayout.addWidget(self.btn_reset)
        self.horizontalLayout.setStretch(0, 4)
        self.horizontalLayout.setStretch(1, 2)
        self.horizontalLayout.setStretch(2, 2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.setStretch(1, 3)

        self.tableWidget.raise_()
        self.btn_reset.raise_()
        self.widget.raise_()

        item = self.tableWidget.verticalHeaderItem(0)
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText("time")
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText("frameID")
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText( "gyro_dx")
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText( "gyro_dy")
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText( "gyro_dz")
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText( "acc_dx")
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText( "acc_dy")
        item = self.tableWidget.horizontalHeaderItem(7)
        item.setText( "acc_dz")
        item = self.tableWidget.horizontalHeaderItem(8)
        item.setText( "gyro_tx")
        item = self.tableWidget.horizontalHeaderItem(9)
        item.setText( "gyro_ty")
        item = self.tableWidget.horizontalHeaderItem(10)
        item.setText( "gyro_tz")
        item = self.tableWidget.horizontalHeaderItem(11)
        item.setText( "acc_tx")
        item = self.tableWidget.horizontalHeaderItem(12)
        item.setText( "acc_ty")
        item = self.tableWidget.horizontalHeaderItem(13)
        item.setText( "acc_tz")

        item = self.tableWidget_2.verticalHeaderItem(0)
        item.setText("Avg_AllData")
        item = self.tableWidget_2.verticalHeaderItem(1)
        item.setText("Avg_100sec")
        item = self.tableWidget_2.verticalHeaderItem(2)
        item.setText("Avg_100sec")
        item = self.tableWidget_2.verticalHeaderItem(3)
        item.setText("Avg_100sec")
        item = self.tableWidget_2.verticalHeaderItem(4)
        item.setText("Avg_100sec")
        item = self.tableWidget_2.verticalHeaderItem(5)
        item.setText("Avg_100sec")
        item = self.tableWidget_2.verticalHeaderItem(5)
        item.setText("Avg_100sec")
        item = self.tableWidget_2.verticalHeaderItem(6)
        item.setText("Avg_100sec")
        item = self.tableWidget_2.horizontalHeaderItem(0)
        item.setText("frameID")
        item = self.tableWidget_2.horizontalHeaderItem(1)
        item.setText("gyro_dx")
        item = self.tableWidget_2.horizontalHeaderItem(2)
        item.setText("gyro_dy")
        item = self.tableWidget_2.horizontalHeaderItem(3)
        item.setText("gyro_dx")
        item = self.tableWidget_2.horizontalHeaderItem(4)
        item.setText("acc_dx")
        item = self.tableWidget_2.horizontalHeaderItem(5)
        item.setText("acc_dy")
        item = self.tableWidget_2.horizontalHeaderItem(6)
        item.setText("acc_dz")

        self.tableWidget.horizontalHeader().resizeSection(0, 100) # 设置首列的宽度
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget_2.setSortingEnabled(False)

        self.btn_reset.setText("复位")
        self.btn_Pause.setText("暂停")

        self.label_starttime.setText("端口启动时间：" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        self.label_duration.setText("运行时长：0")
        self.label_frameCount.setText("接收数据总帧数：0")

        self.avgCount = 1000    # 平均值个数

        self.tDuration = 0
        self.frameCount = 0

        self.drawData = list()
        self.lastData = list()
        self.tableData = list()     # 用于表格显示的实时数据

        self.sumAll = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.avgAll = [0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]        # 用于表格显示的统计数据

        self.sumDuration = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.avgDuartion = list()                              # 用于表格显示的统计数据

        self.refreshFlag = True     # 刷新页面的标志（为false时：数据不更新，显示不更新）
        self.pauseFlag = False      # 暂停刷新标志（为true时：数据更新，计时更新，图、表不更新）

        self.timerC = QTimer(self)
        self.timerC.timeout.connect(self.TimerFrameCount)
        self.timerC.start(1000)

        self.btn_reset.clicked.connect(self.BtnReset)
        self.btn_Pause.clicked[bool].connect(self.BtnPauseTable)
        self.sinOnDraw[list].connect(self.widget.myDraw)

    def BtnReset(self):
        # 暂停刷新
        self.timerC.stop()
        self.refreshFlag = False

        # 计数复位
        self.tDuration = 0
        self.frameCount = 0
        self.label_starttime.setText("端口启动时间：" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        self.label_duration.setText("运行时长：%s 秒" % self.tDuration)
        self.label_frameCount.setText("接收数据总帧数: %s 帧" % self.frameCount)

        # 表格复位
        self.tableData.clear()
        self.sumAll.clear()
        self.sumAll = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.avgAll = [0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.sumDuration = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.avgDuartion.clear()

        self.tableWidget.clearContents()
        self.tableWidget_2.clearContents()

        # 图像复位
        self.drawData.clear()
        self.widget.resetFigure()

        # 开始刷新
        self.timerC.start(1000)
        self.refreshFlag = True

    def BtnPauseTable(self,pressed):
        if pressed:
            self.pauseFlag = True
            self.btn_Pause.setText('继续')
        else:
            self.pauseFlag = False
            self.btn_Pause.setText('暂停')

    def TimerFrameCount(self):
        self.tDuration += 1
        self.label_duration.setText("运行时长：%s"%self.tDuration)
        self.label_frameCount.setText("接收数据总帧数: %s"%self.frameCount)

    def Refresh(self, ld):
        if not self.refreshFlag:
            return
        try:
            for d in ld:
                # 缓存绘图需要的数据
                self.drawData.append(d)
                if len(self.drawData) > 1800:
                    del self.drawData[0]

                self.frameCount += 1    # 可能需要加锁

                # 统计数据
                if d[1]%self.avgCount == 0:  # 10000包数据

                    avg = list()
                    avg.append(d[1]-1)

                    for i in range(6):
                        avg.append(self.sumDuration[i]/self.avgCount)

                    self.avgDuartion.append(avg)
                    if len(self.avgDuartion) > 6:
                        del self.avgDuartion[0]

                    # 重新开始计算和值
                    self.sumDuration = d[2:8].copy()
                else:
                    for i in range(6):
                        self.sumDuration[i] += d[i+2]

                # 总平均
                self.avgAll[0]= d[1]
                for i in range(6):
                    self.sumAll[i] += d[i+2]
                    self.avgAll[i+1] = self.sumAll[i] /self.frameCount

               # 实时数据
                self.tableData.append(d)
                if len(self.tableData) > self.tableRowCount:
                    del self.tableData[0]

            # 刷新表格数据
            if not self.pauseFlag:
                self.tableWidget.clearContents()
                for row in range(len(self.tableData)):
                    for col in range(len(self.tableData[row])):
                        newItem = QtWidgets.QTableWidgetItem(str(self.tableData[row][col]))
                        self.tableWidget.setItem(row, col , newItem)
                self.tableWidget.selectRow(len(self.tableData)-1)

                self.tableWidget_2.clearContents()
                for col in range(len(self.avgAll)):
                    newItem = QtWidgets.QTableWidgetItem(str(self.avgAll[col]))
                    self.tableWidget_2.setItem(0, col, newItem)

                for row in range(len(self.avgDuartion)):
                    for col in range(len(self.avgDuartion[row])):
                        newItem = QtWidgets.QTableWidgetItem(str(self.avgDuartion[row][col]))
                        self.tableWidget_2.setItem(row+1, col, newItem)

            # 发送绘图信号
            if not self.pauseFlag and self.drawData:
                self.sinOnDraw.emit(self.drawData)
                pass



        except Exception as err:
            QMessageBox.information(self, "PorcessInclinometer", str(err), QMessageBox.Ok)
