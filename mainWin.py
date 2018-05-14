# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWin.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(763, 489)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 763, 23))
        self.menubar.setObjectName("menubar")
        self.menu_connect = QtWidgets.QMenu(self.menubar)
        self.menu_connect.setObjectName("menu_connect")
        self.menu_show = QtWidgets.QMenu(self.menubar)
        self.menu_show.setObjectName("menu_show")
        self.menu_save = QtWidgets.QMenu(self.menubar)
        self.menu_save.setObjectName("menu_save")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionClose = QtWidgets.QAction(MainWindow)
        self.actionClose.setObjectName("actionClose")
        self.actionImu = QtWidgets.QAction(MainWindow)
        self.actionImu.setCheckable(True)
        self.actionImu.setEnabled(True)
        self.actionImu.setObjectName("actionImu")
        self.actionInclinometer = QtWidgets.QAction(MainWindow)
        self.actionInclinometer.setCheckable(True)
        self.actionInclinometer.setChecked(True)
        self.actionInclinometer.setObjectName("actionInclinometer")
        self.menu_connect.addAction(self.actionNew)
        self.menu_connect.addSeparator()
        self.menubar.addAction(self.menu_connect.menuAction())
        self.menubar.addAction(self.menu_show.menuAction())
        self.menubar.addAction(self.menu_save.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(-1)
        self.actionNew.triggered.connect(MainWindow.OpenSerial)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Watcher"))
        self.menu_connect.setTitle(_translate("MainWindow", "连接"))
        self.menu_show.setTitle(_translate("MainWindow", "显示"))
        self.menu_save.setTitle(_translate("MainWindow", "保存"))
        self.actionNew.setText(_translate("MainWindow", "New Connect"))
        self.actionClose.setText(_translate("MainWindow", "Close"))
        self.actionImu.setText(_translate("MainWindow", "Imu"))
        self.actionInclinometer.setText(_translate("MainWindow", "Inclinometer"))

