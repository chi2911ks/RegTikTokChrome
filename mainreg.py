from datetime import datetime
import os
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QTableWidgetItem, QLabel, QMessageBox, QInputDialog
from PyQt5 import QtCore, QtGui
from Ui_reg import Ui_RegTikTokChrome
from main import Reg
from win32api import GetSystemMetrics
# import requests
class RegTikTok(Ui_RegTikTokChrome):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(ui)
        self.success = 0
        self.fail = 0

        self.lbTotal = QLabel(self.centralwidget)
        self.lbTotal.setText('<p><span style="font-size:9pt; color: black; font-weight:600;">Tổng: </span> <span style=" color:#ff0000;font-weight:600;">0</span></p>')
        self.lbSuccess = QLabel(self.centralwidget)
        self.lbSuccess.setText('<p><span style="font-size:9pt; color: black; font-weight:600;">Thành công: </span> <span style=" color:#ff0000;font-weight:600;">0</span></p>')
        self.lbFail= QLabel(self.centralwidget)
        self.lbFail.setText('<p><span style="font-size:9pt; color: black; font-weight:600;">Thất bại:</span> <span style=" color:#ff0000;font-weight:600;">0</span></p>')
        self.statusbar.addWidget(self.lbTotal)
        self.statusbar.addWidget(self.lbSuccess)
        self.statusbar.addWidget(self.lbFail)
        self.btnStart.clicked.connect(self.StartReg)
        self.btnStop.clicked.connect(self.StopReg)
        self.btnFolderAvatar.clicked.connect(self.FolderAvatar)
        self.btnFolderChrome.clicked.connect(self.FolderChrome)
        self.btnFileGmail.clicked.connect(self.FileDialogGmail)
        self.pathfileGmail = ""
        self.pathFolder = ""
        self.keyOmo = ""
        self.LoadData()
        self.threadCount.valueChanged.connect(self.SaveData)
        self.versionChrome.valueChanged.connect(self.SaveData)
        self.keyOmocaptcha.textChanged.connect(self.SaveData)
    def SaveData(self):
        
        try:
            self.pathFolder = self.pathAvatar.text()
            self.pathfileGmail = self.pathGmail.text()
            self.keyOmo = self.keyOmocaptcha.text()
            config["SETTINGS"]["pathAvatar"] = self.pathFolder
            config["SETTINGS"]["pathGmail"] = self.pathfileGmail
            config["SETTINGS"]["keyOmocaptcha"] = self.keyOmo
            config["SETTINGS"]["threadCount"] = str(self.threadCount.value())
            config["SETTINGS"]["version"] = str(self.versionChrome.value())
            with open('settings.ini', 'w') as configfile:    
                config.write(configfile)
        except: return
    def LoadData(self):
        try:
            self.pathFolder = config["SETTINGS"]["pathAvatar"]
            self.pathAvatar.setText(self.pathFolder)
            self.pathfileGmail = config["SETTINGS"]["pathGmail"]
            self.pathGmail.setText(self.pathfileGmail)
            self.keyOmo = config["SETTINGS"]["keyOmocaptcha"]
            self.keyOmocaptcha.setText(self.keyOmo)
            self.threadCount.setValue(int(config["SETTINGS"]["threadCount"]))
            self.versionChrome.setValue(int(config["SETTINGS"]["version"]))
        except: return
    def StartReg(self):
        width_scr, height_scr = GetSystemMetrics(0), GetSystemMetrics(1)
        if not os.path.exists(self.pathfileGmail): 
            self.MsgBox('Không tìm thấy file gmail!')
            return
        if self.keyOmo == "":
            self.MsgBox('Vui lòng nhập key omocaptcha!')
            return
        if not os.path.exists(self.pathFolder): 
            self.MsgBox('Không tìm thấy folder avatar!')
            return
        self.btnStart.setEnabled(False)
        self.btnStop.setEnabled(True)
        countFile = 0
        with open(self.pathfileGmail, encoding='utf-8') as file:
            file = file.read().splitlines()
            countFile = len(file)
            self.iterGmail = iter(file)
        self.lbTotal.setText('<p><span style="font-size:9pt; color: black; font-weight:600;">Tổng: </span> <span style=" color:#ff0000;font-weight:600;">%s</span></p>'%countFile)
        index = 0
        index2 = 0
        x = 360
        y = 700
        width = 360
        height = 700
        self.threadReg = {}
        for i in range(self.threadCount.value()):
            if int(width_scr/width) == index: index = 0; y = height; index2 += 1
            if int(height_scr/height) == index2: index = 0; index2 = 0
            self.threadReg[i] = Reg(self, index*x, index2*y)
            self.threadReg[i].start()
            self.threadReg[i].show.connect(self.Show)
            self.threadReg[i].check.connect(self.SetLbStatus)
            self.threadReg[i].finished.connect(self.finishedReg)
            self.Delay(0.1)
            index += 1
            
    def finishedReg(self):
        self.btnStart.setEnabled(True)
        self.btnStop.setEnabled(False)
    def StopReg(self):
        self.finishedReg()
        try:
            for t in self.threadReg.values():t.Stop()
        except: return
    def FileDialogGmail(self):
        file , check = QFileDialog.getOpenFileName(None, "Open File Gmail","", "Text Files (*.txt)")
        if check: self.pathGmail.setText(file); self.SaveData()
    def FolderAvatar(self):
        folder = QFileDialog.getExistingDirectory(None, "Open a folder avatar","./", QFileDialog.ShowDirsOnly)
        if folder != "": self.pathAvatar.setText(folder); self.SaveData()
    def FolderChrome(self):
        folder = QFileDialog.getExistingDirectory(None, "Open a folder avatar","./", QFileDialog.ShowDirsOnly)
        if folder != "": self.pathChrome.setText(folder); self.SaveData()
    def Delay(self, countdelay):
        loop = QtCore.QEventLoop()
        QtCore.QTimer.singleShot(int(countdelay*1000), loop.quit)
        loop.exec()
    def Show(self, row: int, col: int, text: str):
        self.tableWidget.setItem(row, col, QTableWidgetItem(text))
    def SetLbStatus(self, success: bool):
        if success:
            self.success += 1
            self.lbSuccess.setText('<p><span style="font-size:9pt; color: black; font-weight:600;">Thành công: </span> <span style=" color:#ff0000;font-weight:600;">%s</span></p>'%self.success)
        else:
            self.fail += 1
            self.lbFail.setText('<p><span style="font-size:9pt; color: black; font-weight:600;">Thất bại:</span> <span style=" color:#ff0000;font-weight:600;">%s</span></p>'%self.fail)
    def MsgBox(self, text="", icon=QMessageBox.Information):
        self.msg = QMessageBox()
        self.msg.setIcon(icon)
        self.msg.setWindowTitle("Thông báo")
        self.msg.setText(text)
        self.msg.setDefaultButton(QMessageBox.Ok)
        self.msg.setStandardButtons(QMessageBox.Ok)
        self.msg.exec_()
if __name__ == "__main__":
    import sys
    import configparser
    config = configparser.ConfigParser()
    try: config.read('settings.ini') 
    except: pass
    try: config.add_section("SETTINGS")
    except: pass
    app = QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(':/images/icon.ico'))
    ui = QMainWindow()
    cc = RegTikTok()
    ui.show()
    sys.exit(app.exec_())
