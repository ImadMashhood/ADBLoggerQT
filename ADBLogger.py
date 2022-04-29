import inspect
import json
import os
import sys
import subprocess
import multiprocessing
import psutil

from pyadb import ADB
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from subprocess import check_output
from pathvalidate import sanitize_filepath
from datetime import datetime
from qt_thread_updater import get_updater
from PyQt5.QtCore import *

fileName = ""
adb = ADB()
adb.set_adb_path('C:/Users/mashh/AppData/Local/Android/Sdk/platform-tools/adb.exe')

class Ui_MainWindow(object):

    proc = multiprocessing.Process
    isLogging = False

    def __init__(self):
        self.t = None
        self.fileName = None
        self.ipAddress = None
        self.clearPrevLogs = None

    def setupUi(self, MainWindow):

        ######################################
        #           UI Components            #
        ######################################

        #Main Window
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(575, 205)
        MainWindow.setAutoFillBackground(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        #Start Button
        self.startBtn = QtWidgets.QPushButton(self.centralwidget)
        self.startBtn.setGeometry(QtCore.QRect(480, 12, 81, 41))
        self.startBtn.setObjectName("startBtn")
        self.startBtn.clicked.connect(self.startBtnClick)

        #IP Label
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 20, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")

        #IP Text Box
        self.ipAddressTB = QtWidgets.QLineEdit(self.centralwidget)
        self.ipAddressTB.setGeometry(QtCore.QRect(110, 15, 361, 35))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.ipAddressTB.setFont(font)
        self.ipAddressTB.setObjectName("ipAddressTB")

        #File Name Label
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 70, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

        #File Name TB
        self.fileNameTB = QtWidgets.QLineEdit(self.centralwidget)
        self.fileNameTB.setGeometry(QtCore.QRect(110, 65, 361, 35))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.fileNameTB.setFont(font)
        self.fileNameTB.setObjectName("fileNameTB")

        #Stop Button
        self.stopBtn = QtWidgets.QPushButton(self.centralwidget)
        self.stopBtn.setGeometry(QtCore.QRect(480, 62, 81, 41))
        self.stopBtn.setDisabled(True)
        self.stopBtn.setObjectName("stopBtn")
        self.stopBtn.clicked.connect(self.stopBtnClick)

        #Status Label
        self.status = QtWidgets.QLabel(self.centralwidget)
        self.status.setGeometry(QtCore.QRect(110, 130, 361, 41))
        self.status.setText("")
        self.status.setAlignment(QtCore.Qt.AlignCenter)
        self.status.setObjectName("status")

        #Clear Prev Logs Check Box
        self.clearPrevLogsChB = QtWidgets.QCheckBox(self.centralwidget)
        self.clearPrevLogsChB.setGeometry(QtCore.QRect(110, 105, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.clearPrevLogsChB.setFont(font)
        self.clearPrevLogsChB.setObjectName("clearPrevLogsChB")

        #IP Address Combo Box
        self.ipAddressCB = QtWidgets.QComboBox(self.centralwidget)
        self.ipAddressCB.setGeometry(QtCore.QRect(110, 15, 361, 35))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.ipAddressCB.setFont(font)
        self.ipAddressCB.setEditable(True)
        self.ipAddressCB.setVisible(False)
        self.ipAddressCB.setObjectName("ipAddressCB")

        #Progress Bar
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(110, 170, 401, 10))
        self.progressBar.setMaximum(0)
        self.progressBar.setProperty("value", -1)
        self.progressBar.setFormat("")
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setVisible(False)

        #Misc
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 620, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.restoreSettings()
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.startBtn.setText(_translate("MainWindow", "Start"))
        self.label.setText(_translate("MainWindow", "IP Address:"))
        self.ipAddressTB.setPlaceholderText(_translate("MainWindow", "IP Address"))
        self.label_2.setText(_translate("MainWindow", "File Name:"))
        self.fileNameTB.setPlaceholderText(_translate("MainWindow", "File Name"))
        self.stopBtn.setText(_translate("MainWindow", "Stop"))
        self.clearPrevLogsChB.setText(_translate("MainWindow", "Clear Previous Logs"))
        self.ipAddressCB.setPlaceholderText(_translate("MainWindow", "IP Address"))

    def startBtnClick(self):
        self.ipAddress = self.ipAddressTB.text()
        if self.ipAddress == "":
            msg = QMessageBox()
            msg.setWindowTitle("Invalid IP")
            msg.setText("Invalid IP entered, please try again!")
            msg.setIcon(QMessageBox.Warning)
            msg.setInformativeText("You have entered no information in the IP Address field, please enter IP Address.")
            x = msg.exec_()
            return
        self.fileName = self.fileNameTB.text()
        if not self.fileName == sanitize_filepath(self.fileName):
            msg = QMessageBox()
            msg.setWindowTitle("Invalid File Name")
            msg.setText("Invalid file name entered, please try again!")
            msg.setIcon(QMessageBox.Warning)
            msg.setInformativeText("You have entered an invalid file name, would you like your file name cleaned up?")
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            x = msg.exec_()
            if x == QMessageBox.Yes:
                self.fileName = sanitize_filepath(self.fileName)
                self.fileNameTB.setText(self.fileName)
            else:
                return
        if self.fileName == "":
            timeStamp = datetime.now()
            self.fileName = timeStamp.strftime("%d-%m-%Y-%H-%M-%S")+"-logs"
            self.fileName = sanitize_filepath(self.fileName)
            self.fileNameTB.setText(self.fileName)
            app.processEvents()
        self.startBtn.setDisabled(True)
        self.status.setText("Attempting Connection...")
        app.processEvents()
        adb.start_server()
        devices = adb.get_devices()
        adbConnectionAttempt = adb.connect_remote(self.ipAddress, 5555)
        if "failed" in adbConnectionAttempt:
            msg = QMessageBox()
            msg.setWindowTitle("Connection to IP Failed")
            msg.setText("Unable to connect to IP, please try again!")
            msg.setIcon(QMessageBox.Warning)
            msg.setInformativeText("Unable to connect to entered IP Address, please check connection to internet.")
            x = msg.exec_()
            self.stopBtnClick()
            return
        self.stopBtn.setDisabled(False)
        self.progressBar.setVisible(True)
        app.processEvents()
        self.clearPrevLog = self.clearPrevLogsChB.isChecked()
        if self.clearPrevLogs:
            self.status.setText("Clearing Prev Logs")
            app.processEvents()
            adb.get_logcat("-c")
        self.isLogging = True
        self.status.setText("Logging IP Address: " + self.ipAddress)
        self.t = TTT()
        self.t.fileName = self.fileName
        self.t.start()


    def stopBtnClick(self):
        self.progressBar.setVisible(False)
        PROCNAME = "adb.exe"
        for proc in psutil.process_iter():
            if proc.name() == PROCNAME:
                proc.kill()
        self.status.setText("Process Stopped")
        if self.isLogging:
            self.status.setText("Logging complete, file saved")
            self.t.quit_flag = True
            self.t.wait()
            self.saveSettings()
        self.stopBtn.setDisabled(True)
        self.startBtn.setDisabled(False)

    def closeEvent(self, event):
        self.stopBtnClick()
        super(Ui_MainWindow, self).closeEvent(event)

    def saveSettings(self):
        settings = QSettings('verizon', 'adblogger')
        settings.setValue('ipaddress', self.ipAddress)
        settings.setValue('clearprevlogs', self.clearPrevLogs)

    def restoreSettings(self):
        settings = QSettings('verizon', 'adblogger')
        self.ipAddress = settings.value('ipaddress', self.ipAddress)
        self.clearPrevLogs = settings.value('clearprevlogs', self.clearPrevLogs)
        self.ipAddressTB.setText(self.ipAddress)
        self.clearPrevLogsChB.setChecked(bool(self.clearPrevLogs))

class TTT(QThread):
    def __init__(self):
        super(TTT, self).__init__()
        self.quit_flag = False
        self.fileName = ""

    def run(self):
        if not self.quit_flag:
            os.system('cmd /c "adb logcat > '+self.fileName+'.txt')
        self.quit()
        self.wait()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
