# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'incPage.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(714, 322)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.textEdit = QTextEdit_AppendEnable(Form)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.textEdit.setFont(font)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout.addWidget(self.textEdit, 0, 0, 1, 2)
        self.btn_clear = QtWidgets.QPushButton(Form)
        self.btn_clear.setObjectName("btn_clear")
        self.gridLayout.addWidget(self.btn_clear, 1, 1, 1, 1)
        self.btn_stop = QtWidgets.QPushButton(Form)
        self.btn_stop.setCheckable(True)
        self.btn_stop.setChecked(False)
        self.btn_stop.setObjectName("btn_stop")
        self.gridLayout.addWidget(self.btn_stop, 1, 0, 1, 1)
        self.gridLayout.setColumnMinimumWidth(0, 180)
        self.gridLayout.setColumnMinimumWidth(1, 180)
        self.horizontalLayout.addLayout(self.gridLayout)
        self.graphicsView = QtWidgets.QGraphicsView(Form)
        self.graphicsView.setObjectName("graphicsView")
        self.horizontalLayout.addWidget(self.graphicsView)

        self.retranslateUi(Form)
        self.btn_clear.clicked.connect(self.textEdit.clear)
        self.btn_stop.clicked['bool'].connect(Form.Pause)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.btn_clear.setText(_translate("Form", "清空"))
        self.btn_stop.setText(_translate("Form", "暂停"))

from MyWidgets import QTextEdit_AppendEnable
