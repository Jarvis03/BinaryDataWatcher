

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QSizePolicy
from PyQt5.QtCore import QTimer, QThread



import serial

import sys
import os
import struct
import threading
import time
import queue

from MyWidgets import get_time_stamp

from mainWin import Ui_MainWindow
from SerialCfg import Ui_Dialog_SerialCfg
from SelModelDlg import Ui_SelModel
from tabPageInc import tabPage_Inclinometer
from tabPageImu import tabPage_Imu




class SerCfgDlg(QtWidgets.QDialog, Ui_Dialog_SerialCfg):
    def __init__(self,model):
        super().__init__()
        self.setupUi(self)
        if model == 1:
            self.combox_baud.setCurrentIndex(2)
            self.combox_parity.setCurrentIndex(0)
        elif model == 2:
            self.combox_baud.setCurrentIndex(0)
            self.combox_parity.setCurrentIndex(1)
            pass
        else:
            pass

    def GetCfg(self):
        serCfg = (self.combox_port.currentText(), int(self.combox_baud.currentText()),
                       int(self.combox_bytesize.currentText()), self.combox_parity.currentText()[0],
                       float(self.combox_stopbits.currentText()))
        return serCfg

class SelModelDlg(QtWidgets.QDialog, Ui_SelModel):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def GetModel(self):
        if self.radioButton_imu.isChecked():
            return 1
        elif self.radioButton_inc.isChecked():
            return 2
        else:
            return 0

class MainWin(QtWidgets.QMainWindow, Ui_MainWindow):
    sinRefresh = QtCore.pyqtSignal(str,list)

    def __init__(self,model):
        super().__init__()
        self.setupUi(self)

        # 解码模式
        self.workmodel = model  # 1:imu,2:inclinometer
        self.serTimeout = 0.0
        self.serFre = 1
        self.serPackLen = 0
        self.serPackFrm = ''
        self.fileTitle = ''

        self.InitWorkmodel(self.workmodel)

        # 连接配置
        self.serCfgDlg = SerCfgDlg(model)

        # 串口 COM1 serial
        self.serDict = {}

        # 菜单 COM1 action
        self.actCloseDict = { }
        self.actSaveDict = { }

        # table_page
        self.tab_pageDict = { }

        # 接收线程 COM1 thread
        self.threadDict = { }
        self.thRcvFlagDict = { }

        # 文件
        self.saveflagDict = {}
        self.txtfileDayDict = { }   # 当前txt文件的创建时间(天)
        self.txtfileDict = { }
        self.rawfileDict = { }

        self.sinRefresh[str,list].connect(self.RefreshMainWin)

        if not os.path.exists('data'):
            os.makedirs('data')


    def InitWorkmodel(self,model):
        if model == 1:  # imu, len = 48 fre=10 HZ
            self.serTimeout = 1.1
            self.serFre = 10
            self.serPackLen = 48
            self.serPackFrm = '<ccccHHHiiiiiihhhhhhBc'
            self.fileTitle = '[time, frameID, gyro_dx, gyro_dy, gyro_dz, aac_dx, acc_dy, acc_dz, gyro_tx, gyro_ty, gyro_tz, aaa_tx, acc_ty, acc_tz]'
        elif model == 2:  # inclinometer,len = 8, fre = 5 HZ
            self.serTimeout = 1.2
            self.serFre = 5
            self.serPackLen = 8
            self.serPackFrm = '>chhhc'   # 1 + 2*3 + 1 =  8: 0xaa, 0xxx,0xxx,0xxx,0xxx,0xxx,0xxx, 0xff
            self.fileTitle = '[time, inc_x, inc_y, temperature]'
        else:
            pass

    def closeEvent(self, event):
        try:
            if self.serDict:
                reply = QMessageBox.question(self, '退出程序','数据仍在接收，是否退出？', QMessageBox.Yes, QMessageBox.No)
                if reply == QMessageBox.Yes:    # 退出
                    event.accept()
                    portl = list()
                    for port in self.serDict:
                        portl.append(port)
                    for p in portl:
                        self.CloseSerial(p)
                else:
                    event.ignore()
        except Exception as err:
            QMessageBox.information(self, "closeEvent", str(err), QMessageBox.Ok)

    def OpenSerial(self):
        try:
            if self.serCfgDlg.exec() :
                cfg = self.serCfgDlg.GetCfg()
                ser = serial.Serial(*cfg)
                if ser.isOpen():
                    self.serDict[cfg[0]] = ser

                    # 菜单
                    self.AddSerialMenu(cfg[0])

                    # page
                    page = self.NewTabPage(self.workmodel, cfg[0])
                    if page:
                        self.tab_pageDict[cfg[0]] = page
                        self.tabWidget.addTab(page, cfg[0])

                    # file
                    tf = int(time.time())
                    self.txtfileDayDict[cfg[0]] = int(tf/86400)

                    fnametxt =  'data\\' + cfg[0] + '_Data_' + time.strftime("%Y%m%d%H%M%S", time.localtime(tf)) + '.txt'
                    self.txtfileDict[cfg[0]] = open(fnametxt, 'w')
                    self.txtfileDict[cfg[0]].write(self.fileTitle+'\r\n')

                    fnameraw = 'data\\' + cfg[0] + '_Data_' + time.strftime("%Y%m%d%H%M%S", time.localtime()) + '.raw'
                    self.rawfileDict[cfg[0]] = open(fnameraw, 'wb')

                    #thread recv
                    self.threadDict[cfg[0]] = threading.Thread(target=self.Thread_RecvDataFormSerial, args=(cfg[0],), name=cfg[0])
                    self.thRcvFlagDict[cfg[0]] = True
                    self.threadDict[cfg[0]].start()
                else:
                    self.OpenSerial()
        except serial.SerialException as serE:
            QMessageBox.information(self, "OpenSerial", str(serE), QMessageBox.Ok)
            self.OpenSerial()
        except IOError as ioE:
            QMessageBox.information(self, "OpenSerial", str(ioE), QMessageBox.Ok)
            self.serDict[cfg[0]].close()
            self.OpenSerial()
        except Exception as err:
            QMessageBox.information(self, "OpenSerial", str(err), QMessageBox.Ok)


    def CloseSerial(self, serPort):
        try:
            if self.serDict[serPort].isOpen():

                self.thRcvFlagDict[serPort] = False
                self.threadDict[serPort].join()
                del self.thRcvFlagDict[serPort]
                del self.threadDict[serPort]

                self.serDict[serPort].close()
                del self.serDict[serPort]

                self.txtfileDict[serPort].close()
                self.rawfileDict[serPort].close()

                del self.txtfileDict[serPort]
                del self.rawfileDict[serPort]
                del self.saveflagDict[serPort]
                del self.txtfileDayDict[serPort]

                self.DelSerialMenu(serPort)

                self.tab_pageDict[serPort].deleteLater()
                del self.tab_pageDict[serPort]

        except serial.SerialException as e:
            QMessageBox.information(self, "CloseSerial", str(e), QMessageBox.Ok)
        except Exception as err:
            QMessageBox.information(self, "CloseSerial", str(err), QMessageBox.Ok)

    def AddSerialMenu(self,serPort):

        action1 = QtWidgets.QAction(self)
        action1.setObjectName("Close" + serPort)
        self.actCloseDict[serPort] = action1
        action1.setText("Close " + serPort)
        self.menu_connect.addAction(action1)
        action1.triggered.connect(lambda:self.CloseSerial(serPort))

        action3 = QtWidgets.QAction(self)
        action3.setObjectName("Save" + serPort)
        action3.setCheckable(True)
        action3.setChecked(True)
        self.saveflagDict[serPort] = True
        self.actSaveDict[serPort] = action3
        action3.setText("Save " + serPort)
        self.menu_save.addAction(action3)
        action3.triggered.connect(lambda :self.SaveSerial(action3.isChecked(),serPort))

    def DelSerialMenu(self, serPort):
        try:
            self.actCloseDict[serPort].deleteLater()
            del self.actCloseDict[serPort]

            self.actSaveDict[serPort].deleteLater()
            del self.actSaveDict[serPort]

        except Exception as err:
            QMessageBox.information(self, "DelSerialMenu", str(err), QMessageBox.Ok)

    def SaveSerial(self, checked, serPort):
        self.saveflagDict[serPort] = checked

    def NewTabPage(self, model, serPort):
        try:
            if model == 1:
                page = tabPage_Imu()
                page.setObjectName("tab_" + serPort)
                return page
            elif model == 2:
                page = tabPage_Inclinometer()
                page.setObjectName("tab_" + serPort)
                return page
            else:
                pass
        except Exception as err:
            QMessageBox.information(self, "NewTabPage", str(err), QMessageBox.Ok)

    def Thread_RecvDataFormSerial(self, port):

        nReadbytes = self.serFre*self.serPackLen
        remainData = bytes()

        ser = self.serDict[port]
        ser.timeout = self.serTimeout
        ser.flushInput()
        try:
            while self.thRcvFlagDict[port]:
                serdata = ser.read(nReadbytes)

                # 无数据，继续等待接收
                if not serdata:
                    continue

                if self.saveflagDict[port] == True:
                    self.rawfileDict[port].write(serdata)

                serdata = remainData + serdata
                if self.workmodel == 1:
                    remainData = self.PorcessImu(port, serdata)
                elif self.workmodel == 2:
                    remainData = self.PorcessInclinometer(port, serdata)
                else:
                    pass
        except serial.SerialException as serE:
            QMessageBox.information(self, "Thread_RecvDataFormSerial", str(serE), QMessageBox.Ok)
        except IOError as ioE:
            QMessageBox.information(self, "Thread_RecvDataFormSerial", str(ioE), QMessageBox.Ok)
        except Exception as err:
            QMessageBox.information(self, "Thread_RecvDataFormSerial", str(err), QMessageBox.Ok)

    def PorcessInclinometer(self, port, bindata):
        try:
            index = 0
            sendData = list()
            writData = list()

            while 1:
                index = bindata.find(b'\xAA',index)

                # 未找到头
                if index == -1:
                    break

                # 数据长度不足
                if len(bindata[index:]) < self.serPackLen:
                    return bindata[index:]

                # 结尾错误
                if bindata[index+self.serPackLen-1] == b'\xFF':
                    index += 1
                    self.txtfileDict[port].writelines('数据结尾错误！\r\n')
                    continue

                # 解码
                pack = ()
                pack = struct.unpack('>chhhc', bindata[index:index + self.serPackLen])

                # 加入时间标记
                t = time.time()
                lpack = [t, pack[1] / 1000, pack[2] / 1000, pack[3] / 10 ]
                sendData.append(lpack)

                ts = get_time_stamp(t)
                wpack = str([ts, pack[1] / 1000, pack[2] / 1000, pack[3] / 10])
                writData.append(wpack)

                index += self.serPackLen

            if sendData:
                if self.saveflagDict[port]:
                    day = int(sendData[0][0] / 86400)
                    if day > self.txtfileDayDict[port]:
                        self.txtfileDict[port].close()

                        self.txtfileDayDict[port] = day
                        fname = 'data\\' + port + '_Data_' + time.strftime("%Y%m%d%H%M%S", time.localtime(t)) + '.txt'
                        self.txtfileDict[port] = open(fname, 'w')

                    for w in writData:
                        self.txtfileDict[port].writelines(w + '\r\n')

                self.sinRefresh.emit(port, sendData)
            else:
                pass
            return bytes()
        except Exception as err:
            QMessageBox.information(self, "PorcessInclinometer", str(err), QMessageBox.Ok)

    def PorcessImu(self, port, bindata):
        try:
            index = 0
            sendData = list()

            while 1:
                index = bindata.find(b'\xAA\xFF\x55\x01',index)

                # 未找到头
                if index == -1:
                    break

                # 数据长度不足
                if len(bindata[index:]) < self.serPackLen:
                    return bindata[index:]

                # 校验判断
                ck = 0x00
                for b in bindata[index:index + self.serPackLen-2]:
                    ck += b
                if bindata[index+self.serPackLen-1] != ck%256:
                    # 校验错误
                    index += self.serPackLen
                    print('数据包校验错误！！！')
                    continue

                # 解码
                pack = ()
                pack = struct.unpack('<ccccHHHiiiiiihhhhhhBc', bindata[index:index + self.serPackLen])

                # 加入时间戳
                t = time.time()
                ts = get_time_stamp(t)

                # time, frameID, gyro_dx, gyro_dy, gyro_dz, aac_dx, acc_dy, acc_z, gyro_tx, gyro_ty, gyro_tz, aaa_tx, acc_ty, acc_tz
                lpack = [t]
                lpack.append(pack[6])
                for i in range(3):
                    lpack.append(round(pack[7 + i] * 1e-5, 8))
                for i in range(3):
                    lpack.append(round(pack[10 + i] * 1e-7, 8))
                for i in range(6):
                    lpack.append(round(pack[13 + i] * 0.1, 1))
                #print(lpack)

                sendData.append(lpack)

                # 更新index
                index += self.serPackLen

            if self.saveflagDict[port]:
                for l in sendData:
                    self.txtfileDict[port].writelines(str(l) + '\n')

            self.sinRefresh.emit(port, sendData)

            return bytes()
        except Exception as err:
            QMessageBox.information(self, "PorcessImu", str(err), QMessageBox.Ok)

    def RefreshMainWin(self, serPort, ld):
        if serPort in self.tab_pageDict:
            self.tab_pageDict[serPort].Refresh(ld)

        # 加入刷新状态栏
        pass

    def reset_figure(self,serPort):
        if serPort in self.tab_pageDict:
            pass



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    selDlg = SelModelDlg()
    selDlg.show()
    if selDlg.exec():

        model = selDlg.GetModel()
        mwin = MainWin(model)
        mwin.show()
        sys.exit(app.exec_())