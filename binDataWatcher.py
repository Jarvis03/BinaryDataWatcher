

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QSizePolicy
from PyQt5.QtCore import QTimer



import serial

import sys
import os
import struct
import threading
import time
import queue

from mainWin import Ui_MainWindow
from SerialCfg import Ui_Dialog_SerialCfg
from SelModelDlg import Ui_SelModel

from MyWidgets import tabPage_Inclinometer
from MyWidgets import tabPage_Imu
from MyWidgets import get_time_stamp



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
        self.actShowDict = { }
        self.actSaveDict = { }

        # table_page
        self.tab_pageDict = { }

        # 接收线程 COM1 thread
        self.threadDict = { }
        self.thRcvFlagDict = { }

        # 显示线程
        self.thGetData = threading.Thread()
        self.thGetFlag = False

        # 数据（解码->处理显示）的队列
        self.dataQueue = { }
        self.imuTempData = { }

        # 是否存储
        self.saveflagDict = { }

        # 文件
        self.txtfileDayDict = { }      # 当前文件时间
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
            self.fileTitle = '[time, frameID, gyro_dx, gyro_dy, gyro_dz, aac_dx, acc_dy, acc_dz, gyro_tx, gyro_ty, gyro_tz, aaa_tx, acc_ty, acc_tz, ' \
                             'gyro_dxAvg, gyro_dyAvg, gyro_dzAvg, acc_dxAvg, acc_dxAvg, acc_dzAvg]'
        elif model == 2:  # inclinometer,len = 8, fre = 5 HZ
            self.serTimeout = 1.2
            self.serFre = 5
            self.serPackLen = 8
            self.serPackFrm = '>chhhc'   # 1 + 2*3 + 1 =  8: 0xaa, 0xxx,0xxx,0xxx,0xxx,0xxx,0xxx, 0xff
            self.fileTitle = '[time, inc_x, inc_y, temperature]'
        else:
            pass

    def closeEvent(self, *args, **kwargs):
        try:
            # 停止线程
            self.thGetFlag = False
            self.thGetData.join()

            for t in self.threadDict:
                self.thRcvFlagDict[t] = False
                self.threadDict[t].join()

            # 关闭文件
            for f in self.txtfileDict:
                self.rawfileDict[f].close()
                self.txtfileDict[f].close()

            # 关闭串口
            for s in self.serDict:
                self.serDict[s].close()
        except Exception as err:
            QMessageBox.information(self, "closeEvent", str(err), QMessageBox.Ok)

    def OpenSerial(self):
        bQuit = True
        if self.serCfgDlg.exec() :
            cfg = self.serCfgDlg.GetCfg()
            try:
                ser = serial.Serial(*cfg)
                if ser.isOpen():
                    self.serDict[cfg[0]] = ser
                    self.AddSerialMenu(cfg[0])

                    # 创建数据
                    self.dataQueue[cfg[0]] = queue.Queue(100)

                    # 缓存imu数据（100s*0HZ）
                    self.imuTempData[cfg[0]] = list()

                    # 创建文件
                    tf = int(time.time())
                    self.txtfileDayDict[cfg[0]] = int(tf/86400)
                    fnamet =  'data\\' + cfg[0] + '_Data_' + time.strftime("%Y%m%d%H%M%S", time.localtime(tf)) + '.txt'

                    self.txtfileDict[cfg[0]] = open(fnamet, 'w')
                    self.txtfileDict[cfg[0]].write(self.fileTitle+'\r\n')
                    fnamer = 'data\\' + cfg[0] + '_Data_' + time.strftime("%Y%m%d%H%M%S", time.localtime()) + '.raw'
                    self.rawfileDict[cfg[0]] = open(fnamer, 'wb')

                    # 创建线程
                    if not self.thGetFlag:
                        self.thGetData = threading.Thread(target=self.Thread_GetData)
                        self.thGetFlag = True
                        self.thGetData.start()

                    th = threading.Thread(target=self.Thread_RecvDataFormSerial, args=(cfg[0],), name=cfg[0])
                    self.threadDict[cfg[0]] = th
                    self.thRcvFlagDict[cfg[0]] = True
                    self.threadDict[cfg[0]].start()

                else:
                    bQuit = True
            except serial.SerialException as serE:
                QMessageBox.information(self, "打开串口失败", str(serE), QMessageBox.Ok)
                bQuit = False
            except IOError as ioE:
                QMessageBox.information(self, "创建文件失败", str(ioE), QMessageBox.Ok)
                self.serDict[cfg[0]].close()
            except Exception as err:
                QMessageBox.information(self, "OpenSerial", str(err), QMessageBox.Ok)
                return
        if not bQuit:
            self.OpenSerial()

    def CloseSerial(self, serPort):
        try:
            if self.serDict[serPort].isOpen():
                # 停止接收
                self.thRcvFlagDict[serPort] = False
                self.threadDict[serPort].join()
                del self.thRcvFlagDict[serPort]
                del self.threadDict[serPort]
                # 关闭串口
                self.serDict[serPort].close()
                del self.serDict[serPort]
                if not self.serDict:
                    self.thGetFlag = False
                    self.thGetData.join()
                # 关闭文件
                time.sleep(0.1) # 等待缓存的数据写入（文件和控件）
                self.txtfileDict[serPort].close()
                self.rawfileDict[serPort].close()
                del self.txtfileDict[serPort]
                del self.rawfileDict[serPort]
                del self.saveflagDict[serPort]
                del self.dataQueue[serPort]

                self.DelSerialMenu(serPort)
        except serial.SerialException as e:
            QMessageBox.information(self, "关闭串口失败", str(e), QMessageBox.Ok)
        except Exception as err:
            QMessageBox.information(self, "CloseSerial", str(err), QMessageBox.Ok)

    def AddSerialMenu(self,serPort):
        # close
        action1 = QtWidgets.QAction(self)
        action1.setObjectName("Close" + serPort)
        self.actCloseDict[serPort] = action1
        action1.setText("Close " + serPort)
        self.menu_connect.addAction(action1)
        action1.triggered.connect(lambda:self.CloseSerial(serPort))

        # show
        action2 = QtWidgets.QAction(self)
        action2.setObjectName("Show" + serPort)
        self.actShowDict[serPort] = action2
        action2.setText("Show " + serPort)
        self.menu_show.addAction(action2)
        action2.triggered.connect(lambda: self.ShowSerial(serPort))

        # Save
        action3 = QtWidgets.QAction(self)
        action3.setObjectName("Save" + serPort)
        action3.setCheckable(True)
        action3.setChecked(True)
        self.saveflagDict[serPort] = True
        self.actSaveDict[serPort] = action3
        action3.setText("Save " + serPort)
        self.menu_save.addAction(action3)
        action3.triggered.connect(lambda :self.SaveSerial(action3.isChecked(),serPort))

        # tabWidget
        page = self.NewTabPage(self.workmodel, serPort)
        if page:
            self.tab_pageDict[serPort] = page
            self.tabWidget.addTab(page, serPort)

    def DelSerialMenu(self, serPort):
        try:
            # 删除菜单项
            self.actCloseDict[serPort].deleteLater()
            del self.actCloseDict[serPort]

            self.actShowDict[serPort].deleteLater()
            del self.actShowDict[serPort]

            self.actSaveDict[serPort].deleteLater()
            del self.actSaveDict[serPort]

            # 删除显示页面
            self.tab_pageDict[serPort].deleteLater()
            del self.tab_pageDict[serPort]
        except Exception as err:
            QMessageBox.information(self, "DelSerialMenu", str(err), QMessageBox.Ok)

    def ShowSerial(self,serPort):
        pass

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
        remainData = bytes()
        serData = bytes()
        nReadbytes = self.serFre*self.serPackLen

        ser = self.serDict[port]
        ser.timeout = self.serTimeout
        ser.flushInput()
        try:
            while self.thRcvFlagDict[port]:
                serData = ser.read(nReadbytes)

                # 无数据，继续等待接收
                if not serData:
                    continue

                # 存储原始数据
                if self.saveflagDict[port] == True:
                    self.rawfileDict[port].write(serData)

                # 拼包、处理
                serData = remainData + serData
                if self.workmodel == 1:
                    remainData = self.PorcessImu(port, serData)
                elif self.workmodel == 2:
                    remainData = self.PorcessInclinometer(port, serData)
                else:
                    pass
        except serial.SerialException as serE:
            QMessageBox.information(self, "串口接收异常", str(serE), QMessageBox.Ok)
        except IOError as ioE:
            QMessageBox.information(self, "", str(ioE), QMessageBox.Ok)
        except Exception as err:
            QMessageBox.information(self, "Thread_RecvDataFormSerial", str(err), QMessageBox.Ok)

    def Thread_GetData(self):
        try:
            while self.thGetFlag:
                for p in self.dataQueue:
                    data = list()
                    while True:
                        try:
                            data.append(self.dataQueue[p].get_nowait())
                        except queue.Empty:
                            break
                    # 实时显示
                    self.sinRefresh.emit(p, data)
                time.sleep(1)
        except Exception as err:
            QMessageBox.information(self, "Thread_GetData", str(err), QMessageBox.Ok)

    def PorcessInclinometer(self, port, bindata):
        try:
            index = 0
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
                    continue

                # 解码
                pack = ()
                pack = struct.unpack('>chhhc', bindata[index:index + self.serPackLen])

                # 加入时间标记
                t = time.time()
                ts = get_time_stamp(t)
                lpack = [t, pack[1] / 1000, pack[2] / 1000, pack[3] / 10 ]
                wpack = str([ts, pack[1] / 1000, pack[2] / 1000, pack[3] / 10])
                self.dataQueue[port].put(lpack)

                # 解码后的数据存文件
                day = int(t/86400)
                if day != self.txtfileDayDict[port]:
                    self.txtfileDict[port].close()

                    self.txtfileDayDict[port] = day
                    fname = 'data\\' + port + '_Data_' + time.strftime("%Y%m%d%H%M%S", time.localtime(t)) + '.txt'

                    self.txtfileDict[port] = open(fname, 'w')
                if self.saveflagDict[port] == True:
                    self.txtfileDict[port].writelines(wpack+'\n')
                index += self.serPackLen
            return bytes()
        except Exception as err:
            QMessageBox.information(self, "PorcessInclinometer", str(err), QMessageBox.Ok)

    def PorcessImu(self, port, bindata):
        try:
            index = 0
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

                lpack = list()
                # lpack 内容
                # time, frameID, gyro_dx, gyro_dy, gyro_dz, aac_dx, acc_dy, acc_z, gyro_tx, gyro_ty, gyro_tz, aaa_tx, acc_ty, acc_tz
                lpack.append(pack[6])
                for i in range(6):
                    lpack.append(round(pack[7 + i] * 1e-5, 8))
                for i in range(6):
                    lpack.append(round(pack[13 + i] * 0.1, 1))

                lpack.insert(0, t)

                # 加入解码完成的队列
                self.dataQueue[port].put(lpack)
                #print(lpack)

                # 写入缓存数据
                self.imuTempData[port].append(lpack)

                # 是否需要写文件（1000一次）
                if self.imuTempData[port][-1][1] % 1000 == 0:
                    lavg = self.calculateAverage(port)

                    # 写文件
                    for l in self.imuTempData[port]:
                        self.txtfileDict[port].writelines(str(l + lavg) + '\n')

                    # 清空缓存数据
                    self.imuTempData[port] = list()

                # 更新index
                index += self.serPackLen

            return bytes()
        except Exception as err:
            QMessageBox.information(self, "PorcessInclinometer", str(err), QMessageBox.Ok)

    def calculateAverage(self, port):
        # 计算当前所有已解析数据的均值
        lc = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        for l in self.imuTempData[port]:
            for i in range(6):
                lc[i] += l[i + 2]
        for l in range(6):
            lc[l] = round(lc[l] / len(self.imuTempData[port]), 6)
        return lc

    def RefreshMainWin(self, serPort, ld):
        # 刷新状态栏
        pass

        # 刷新 tabpage
        if serPort in self.tab_pageDict:
            self.tab_pageDict[serPort].Refresh(ld)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    selDlg = SelModelDlg()
    selDlg.show()
    if selDlg.exec():

        model = selDlg.GetModel()
        mwin = MainWin(model)
        mwin.show()
        sys.exit(app.exec_())