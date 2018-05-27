
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QSizePolicy, QVBoxLayout, QLineEdit, QMessageBox

from MyWidgets import MyFigure_Inc
from MyWidgets import QTextEdit_AppendEnable


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


    def Pause(self,pressed):
        if pressed:
            self.btn_stop.setText('继续')
            self.textEdit.setAppendeEnable(False)
        else:
            self.btn_stop.setText('暂停')
            self.textEdit.setAppendeEnable(True)
