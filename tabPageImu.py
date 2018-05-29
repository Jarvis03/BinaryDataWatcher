from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QSizePolicy, QVBoxLayout, QLineEdit, QMessageBox
from PyQt5.QtCore import QTimer, QThread

from MyWidgets import MyFigure_Imu

import time

class tabPage_Imu(QtWidgets.QWidget):
    sinOnDraw = QtCore.pyqtSignal(list)
    sinResetDarw = QtCore.pyqtSignal()

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
        self.tableWidget.setRowCount(0)
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

        self.tDuration = 0      # 数据接收时长
        self.frameCount = 0     # 数据帧计数

        self.drawData = list()

        self.refreshFlag = True  # 刷新页面的标志（为false时：数据不更新，显示不更新）
        self.pauseFlag = False  # 暂停刷新标志（为true时：数据更新，计时更新，图、表不更新）

        self.timerC = QTimer(self)
        self.timerC.timeout.connect(self.TimerFrameCount)
        self.timerC.start(1000)

        self.btn_reset.clicked.connect(self.BtnReset)
        self.btn_Pause.clicked[bool].connect(self.BtnPauseTable)
        self.sinOnDraw[list].connect(self.widget.on_draw)
        self.sinResetDarw.connect(self.widget.reset_draw)

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

        # 图像复位
        self.sinResetDarw.emit()

        # 表格复位
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)

        # 开始刷新
        self.timerC.start(1000)
        self.refreshFlag = True

    def BtnPauseTable(self, pressed):
        if pressed:
            self.pauseFlag = True
            self.btn_Pause.setText('继续')
        else:
            self.pauseFlag = False
            self.btn_Pause.setText('暂停')

    def TimerFrameCount(self):
        self.tDuration += 1
        self.label_duration.setText("运行时长：%s" % self.tDuration)
        self.label_frameCount.setText("接收数据总帧数: %s" % self.frameCount)

    def Refresh(self, ld):
        if not self.refreshFlag:
            return

        if not ld:
            return

        try:
            for d in ld:
                self.drawData.append(d)
                self.frameCount += 1

                if not self.pauseFlag:
                    row = self.tableWidget.rowCount()
                    self.tableWidget.insertRow(row)
                    for col in range(self.tableColCount):
                        newItem = QtWidgets.QTableWidgetItem(str(d[col]))
                        self.tableWidget.setItem(row, col, newItem)

                    if row == self.tableRowCount: # 表格已满，向上滚动一行
                        self.tableWidget.removeRow(0)

            if not self.pauseFlag:
                self.tableWidget.selectRow(self.tableWidget.rowCount() - 1)

                self.sinOnDraw.emit(self.drawData)
                self.drawData.clear()

        except Exception as err:
            QMessageBox.information(self, "Refresh", str(err), QMessageBox.Ok)

