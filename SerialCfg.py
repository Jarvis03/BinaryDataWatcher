# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SerialCfg.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog_SerialCfg(object):
    def setupUi(self, Dialog_SerialCfg):
        Dialog_SerialCfg.setObjectName("Dialog_SerialCfg")
        Dialog_SerialCfg.setWindowModality(QtCore.Qt.NonModal)
        Dialog_SerialCfg.resize(231, 223)
        Dialog_SerialCfg.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        Dialog_SerialCfg.setAcceptDrops(False)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog_SerialCfg)
        self.buttonBox.setGeometry(QtCore.QRect(30, 185, 186, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.groupBox = QtWidgets.QGroupBox(Dialog_SerialCfg)
        self.groupBox.setGeometry(QtCore.QRect(15, 15, 201, 161))
        self.groupBox.setObjectName("groupBox")
        self.combox_bytesize = QtWidgets.QComboBox(self.groupBox)
        self.combox_bytesize.setGeometry(QtCore.QRect(105, 75, 61, 20))
        self.combox_bytesize.setMinimumSize(QtCore.QSize(0, 0))
        self.combox_bytesize.setObjectName("combox_bytesize")
        self.combox_bytesize.addItem("")
        self.combox_bytesize.addItem("")
        self.combox_bytesize.addItem("")
        self.combox_bytesize.addItem("")
        self.combox_baud = QtWidgets.QComboBox(self.groupBox)
        self.combox_baud.setGeometry(QtCore.QRect(105, 50, 61, 20))
        self.combox_baud.setMinimumSize(QtCore.QSize(0, 0))
        self.combox_baud.setObjectName("combox_baud")
        self.combox_baud.addItem("")
        self.combox_baud.addItem("")
        self.combox_baud.addItem("")
        self.label_1 = QtWidgets.QLabel(self.groupBox)
        self.label_1.setGeometry(QtCore.QRect(35, 20, 51, 25))
        self.label_1.setMinimumSize(QtCore.QSize(0, 0))
        self.label_1.setObjectName("label_1")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(35, 95, 46, 25))
        self.label_4.setMinimumSize(QtCore.QSize(46, 23))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(35, 120, 46, 25))
        self.label_5.setMinimumSize(QtCore.QSize(46, 23))
        self.label_5.setObjectName("label_5")
        self.combox_stopbits = QtWidgets.QComboBox(self.groupBox)
        self.combox_stopbits.setGeometry(QtCore.QRect(105, 125, 61, 20))
        self.combox_stopbits.setMinimumSize(QtCore.QSize(0, 0))
        self.combox_stopbits.setObjectName("combox_stopbits")
        self.combox_stopbits.addItem("")
        self.combox_stopbits.addItem("")
        self.combox_stopbits.addItem("")
        self.combox_parity = QtWidgets.QComboBox(self.groupBox)
        self.combox_parity.setGeometry(QtCore.QRect(105, 100, 61, 20))
        self.combox_parity.setMinimumSize(QtCore.QSize(0, 0))
        self.combox_parity.setObjectName("combox_parity")
        self.combox_parity.addItem("")
        self.combox_parity.addItem("")
        self.combox_parity.addItem("")
        self.combox_parity.addItem("")
        self.combox_parity.addItem("")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(35, 45, 46, 25))
        self.label_2.setMinimumSize(QtCore.QSize(46, 23))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(35, 70, 46, 25))
        self.label_3.setMinimumSize(QtCore.QSize(46, 23))
        self.label_3.setObjectName("label_3")
        self.combox_port = QComboBox_SelSerialNum(self.groupBox)
        self.combox_port.setGeometry(QtCore.QRect(105, 25, 61, 20))
        self.combox_port.setMinimumSize(QtCore.QSize(0, 0))
        self.combox_port.setObjectName("combox_port")
        self.combox_port.addItem("")

        self.retranslateUi(Dialog_SerialCfg)
        self.combox_parity.setCurrentIndex(1)
        self.buttonBox.accepted.connect(Dialog_SerialCfg.accept)
        self.buttonBox.rejected.connect(Dialog_SerialCfg.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog_SerialCfg)

    def retranslateUi(self, Dialog_SerialCfg):
        _translate = QtCore.QCoreApplication.translate
        Dialog_SerialCfg.setWindowTitle(_translate("Dialog_SerialCfg", "新建连接"))
        self.groupBox.setTitle(_translate("Dialog_SerialCfg", "串口连接配置"))
        self.combox_bytesize.setItemText(0, _translate("Dialog_SerialCfg", "8"))
        self.combox_bytesize.setItemText(1, _translate("Dialog_SerialCfg", "7"))
        self.combox_bytesize.setItemText(2, _translate("Dialog_SerialCfg", "6"))
        self.combox_bytesize.setItemText(3, _translate("Dialog_SerialCfg", "5"))
        self.combox_baud.setItemText(0, _translate("Dialog_SerialCfg", "9600"))
        self.combox_baud.setItemText(1, _translate("Dialog_SerialCfg", "38400"))
        self.combox_baud.setItemText(2, _translate("Dialog_SerialCfg", "115200"))
        self.label_1.setText(_translate("Dialog_SerialCfg", "串口号："))
        self.label_4.setText(_translate("Dialog_SerialCfg", "校验位："))
        self.label_5.setText(_translate("Dialog_SerialCfg", "停止位："))
        self.combox_stopbits.setItemText(0, _translate("Dialog_SerialCfg", "1"))
        self.combox_stopbits.setItemText(1, _translate("Dialog_SerialCfg", "1.5"))
        self.combox_stopbits.setItemText(2, _translate("Dialog_SerialCfg", "2"))
        self.combox_parity.setItemText(0, _translate("Dialog_SerialCfg", "None"))
        self.combox_parity.setItemText(1, _translate("Dialog_SerialCfg", "EVEN"))
        self.combox_parity.setItemText(2, _translate("Dialog_SerialCfg", "ODD"))
        self.combox_parity.setItemText(3, _translate("Dialog_SerialCfg", "MARK"))
        self.combox_parity.setItemText(4, _translate("Dialog_SerialCfg", "SPACE"))
        self.label_2.setText(_translate("Dialog_SerialCfg", "波特率："))
        self.label_3.setText(_translate("Dialog_SerialCfg", "数据位："))
        self.combox_port.setItemText(0, _translate("Dialog_SerialCfg", "None"))

from MyWidgets import QComboBox_SelSerialNum