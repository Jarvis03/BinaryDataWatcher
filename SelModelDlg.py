# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SelModelDlg.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SelModel(object):
    def setupUi(self, SelModel):
        SelModel.setObjectName("SelModel")
        SelModel.resize(386, 208)
        self.buttonBox = QtWidgets.QDialogButtonBox(SelModel)
        self.buttonBox.setGeometry(QtCore.QRect(25, 160, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(SelModel)
        self.label.setGeometry(QtCore.QRect(25, 25, 106, 16))
        self.label.setObjectName("label")
        self.radioButton_imu = QtWidgets.QRadioButton(SelModel)
        self.radioButton_imu.setGeometry(QtCore.QRect(75, 65, 256, 16))
        self.radioButton_imu.setObjectName("radioButton_imu")
        self.radioButton_inc = QtWidgets.QRadioButton(SelModel)
        self.radioButton_inc.setGeometry(QtCore.QRect(75, 100, 186, 16))
        self.radioButton_inc.setChecked(True)
        self.radioButton_inc.setObjectName("radioButton_inc")

        self.retranslateUi(SelModel)
        self.buttonBox.accepted.connect(SelModel.accept)
        self.buttonBox.rejected.connect(SelModel.reject)
        QtCore.QMetaObject.connectSlotsByName(SelModel)

    def retranslateUi(self, SelModel):
        _translate = QtCore.QCoreApplication.translate
        SelModel.setWindowTitle(_translate("SelModel", "工作模式"))
        self.label.setText(_translate("SelModel", "请选择工作模式："))
        self.radioButton_imu.setText(_translate("SelModel", "Imu：解析并显示惯性测量单元的数据流"))
        self.radioButton_inc.setText(_translate("SelModel", "Inc：解析并显示倾斜仪数据流"))

