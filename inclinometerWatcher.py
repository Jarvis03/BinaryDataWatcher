

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QSizePolicy



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

from MyWidgets import  MyMplCanvas





class SerCfgDlg(QtWidgets.QDialog, Ui_Dialog_SerialCfg):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

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

        self.serCfgDlg = SerCfgDlg()

        # 解码模式
        self.workmodel = model  # 1:imu,2:inclinometer
        self.InitWorkmodel(self.workmodel)

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

        # 数据
        self.txtdataDict = { }

        # 是否存储
        self.saveflagDict = { }

        # 文件
        self.txtfileDict = { }
        self.rawfileDict = { }

        self.sinRefresh[str,list].connect(self.RefreshEdit)
        self.sinRefresh[str, list].connect(self.DrawGraph)

        if not os.path.exists('data'):
            os.makedirs('data')

    def InitWorkmodel(self,model):
        if model == 1:  # imu, len = 48 fre=10 HZ
            self.serTimeout = 1.1
            self.serFre = 10
            self.serPackLen = 48
            self.serPackFrm = '<ccccHHHiiiiiihhhhhhBc'
        elif model == 2:  # inclinometer,len = 8, fre = 5 HZ
            self.serTimeout = 1.2
            self.serFre = 5
            self.serPackLen = 8
            self.serPackFrm = '>chhhc'   # 1 + 2*3 + 1 =  8: 0xaa, 0xxx,0xxx,0xxx,0xxx,0xxx,0xxx, 0xff
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

                    # 创建数据存储(最长缓存36000条数据)
                    self.txtdataDict[cfg[0]] = queue.Queue(36000)

                    # 创建文件
                    fnamet =  'data\\' + cfg[0] + '_Data_' + time.strftime("%Y%m%d%H%M%S", time.localtime()) + '.txt'
                    self.txtfileDict[cfg[0]] = open(fnamet, 'w')
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
                del self.txtdataDict[serPort]
                del self.saveflagDict[serPort]

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
                pass
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
                for p in self.serDict:
                    data = list()
                    while True:
                        try:
                            data.append(self.txtdataDict[p].get_nowait())
                        except queue.Empty:
                            break
                    # 实时显示
                    self.sinRefresh.emit(p,data)
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
                t,ts = self.get_time_stamp()
                lpack = str([ts, pack[1] / 1000, pack[2] / 1000, pack[3] / 10 ])
                #print(lpack)

                self.txtdataDict[port].put(lpack)

                # 解码后的数据存文件
                if int(t) % 86400 == 0:
                    self.txtfileDict[port].close()
                    self.txtfileDict[port] = open('data\\' + port + '_Data_' + time.strftime("%Y%m%d%H%M%S", time.localtime()) + '.txt', 'w')
                if self.saveflagDict[port] == True:
                    self.txtfileDict[port].writelines(lpack+'\n')
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

                # 校验错误
                # ck = 0x00
                # for b in bindata[index:index + self.serPackLen-1]:
                #     ck += b
                # if bindata[index+self.serPackLen-1] != ck:
                #     continue

                # 解码
                pack = ()
                pack = struct.unpack('<ccccHHHiiiiiihhhhhhBc', bindata[index:index + self.serPackLen])

                # 加入时间戳
                t, ts = self.get_time_stamp()

                lpack = list()
                lpack.append(t)
                lpack.append(pack[6])
                for i in range(6):
                    lpack.append(round(pack[7 + i] * 1e-5, 8))
                for i in range(6):
                    lpack.append(round(pack[13 + i] * 0.1, 1))

                lpack = str(lpack)
                print(lpack)

                self.txtdataDict[port].put(lpack)

                if self.saveflagDict[port] == True:
                    self.txtfileDict[port].writelines(lpack+'\n')
                index += self.serPackLen
            return bytes()
        except Exception as err:
            QMessageBox.information(self, "PorcessInclinometer", str(err), QMessageBox.Ok)

    def RefreshEdit(self,serPort,ld):
        if serPort not in self.tab_pageDict:
            return
        try:
            for d in ld:
                self.tab_pageDict[serPort].textEdit.append(d)
        except Exception as err:
            QMessageBox.information(self, "RefreshEdit", str(err), QMessageBox.Ok)

    def DrawGraph(self,serPort,ld):
        pass

    def get_time_stamp(self):
        ct = time.time()
        local_time = time.localtime(ct)
        data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
        data_secs = (ct - int(ct)) * 1000
        time_stamp = "%s.%03d" % (data_head, data_secs)

        return ct, time_stamp





if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    selDlg = SelModelDlg()
    selDlg.show()
    if selDlg.exec():

        model = selDlg.GetModel()
        mwin = MainWin(model)
        mwin.show()
        sys.exit(app.exec_())