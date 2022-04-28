import os
import sys
import subprocess
import multiprocessing

from pyadb import ADB
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from subprocess import check_output
from pathvalidate import sanitize_filepath
from datetime import datetime



class Ui_MainWindow(object):

    proc = multiprocessing.Process
    isLogging = False

    def setupUi(self, MainWindow):

        ######################################
        #           UI Components            #
        ######################################

        #Main Window
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(620, 280)
        MainWindow.setAutoFillBackground(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        #Start Button
        self.startBtn = QtWidgets.QPushButton(self.centralwidget)
        self.startBtn.setGeometry(QtCore.QRect(510, 20, 81, 41))
        self.startBtn.setObjectName("startBtn")
        self.startBtn.clicked.connect(self.startBtnClick)

        #IP Label
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 30, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")

        #IP Text Box
        self.ipAddressTB = QtWidgets.QLineEdit(self.centralwidget)
        self.ipAddressTB.setGeometry(QtCore.QRect(130, 25, 361, 35))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.ipAddressTB.setFont(font)
        self.ipAddressTB.setObjectName("ipAddressTB")

        #File Name Label
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 90, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

        #File Name TB
        self.fileNameTB = QtWidgets.QLineEdit(self.centralwidget)
        self.fileNameTB.setGeometry(QtCore.QRect(130, 85, 361, 35))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.fileNameTB.setFont(font)
        self.fileNameTB.setObjectName("fileNameTB")

        #Stop Button
        self.stopBtn = QtWidgets.QPushButton(self.centralwidget)
        self.stopBtn.setGeometry(QtCore.QRect(510, 80, 81, 41))
        self.stopBtn.setDisabled(True)
        self.stopBtn.setObjectName("stopBtn")
        self.stopBtn.clicked.connect(self.stopBtnClick)

        #Status Label
        self.status = QtWidgets.QLabel(self.centralwidget)
        self.status.setGeometry(QtCore.QRect(130, 180, 361, 41))
        self.status.setText("")
        self.status.setAlignment(QtCore.Qt.AlignCenter)
        self.status.setObjectName("status")

        #Clear Prev Logs Check Box
        self.clearPrevLogsChB = QtWidgets.QCheckBox(self.centralwidget)
        self.clearPrevLogsChB.setGeometry(QtCore.QRect(130, 130, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.clearPrevLogsChB.setFont(font)
        self.clearPrevLogsChB.setObjectName("clearPrevLogsChB")

        #IP Address Combo Box
        self.ipAddressCB = QtWidgets.QComboBox(self.centralwidget)
        self.ipAddressCB.setGeometry(QtCore.QRect(130, 25, 361, 35))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.ipAddressCB.setFont(font)
        self.ipAddressCB.setEditable(True)
        self.ipAddressCB.setVisible(False)
        self.ipAddressCB.setObjectName("ipAddressCB")

        #Progress Bar
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(130, 240, 401, 16))
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
        # adb = ADB()
        # adb.set_adb_path('C:/Users/mashh/AppData/Local/Android/Sdk/platform-tools/adb.exe')
        ipAddress = self.ipAddressTB.text()
        if ipAddress == "":
            msg = QMessageBox()
            msg.setWindowTitle("Invalid IP")
            msg.setText("Invalid IP entered, please try again!")
            msg.setIcon(QMessageBox.Warning)
            msg.setInformativeText("You have entered no information in the IP Address field, please enter IP Address.")
            x = msg.exec_()
            return
        fileName = self.fileNameTB.text()
        if not fileName == sanitize_filepath(fileName):
            msg = QMessageBox()
            msg.setWindowTitle("Invalid File Name")
            msg.setText("Invalid file name entered, please try again!")
            msg.setIcon(QMessageBox.Warning)
            msg.setInformativeText("You have entered an invalid file name, would you like your file name cleaned up?")
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            x = msg.exec_()
            if x == QMessageBox.Yes:
                fileName = sanitize_filepath(fileName)
                self.fileNameTB.setText(fileName)
            else:
                return
        if fileName == "":
            timeStamp = datetime.now()
            fileName = timeStamp.strftime("%d/%m/%Y %H-%M-%S")+"-logs"
            fileName = sanitize_filepath(fileName)
            self.fileNameTB.setText(fileName)
        self.startBtn.setDisabled(True)
        self.stopBtn.setDisabled(False)
        self.progressBar.setVisible(True)
        self.proc = multiprocessing.Process(self.startBtnADBCalls(ipAddress, fileName), args=(10,))
        self.proc.start()

    def stopBtnClick(self):
        self.proc.terminate()
        self.progressBar.setVisible(False)
        os.system("taskkill /f /im adb.exe")
        self.status.setText("Process Stopped")
        if self.isLogging:
            self.status.setText("Logging complete, file saved")
    #print(check_output(["adb", "connect", ipAddress]))

    def startBtnADBCalls(self, ipAddress, fileName):
        self.status.setText("Attempting Connection")
        adbConnectionAttempt = str(check_output(["adb", "connect", ipAddress]))
        print(adbConnectionAttempt)
        if not "connected" in adbConnectionAttempt:
            msg = QMessageBox()
            msg.setWindowTitle("Connection to IP Failed")
            msg.setText("Unable to connect to IP, please try again!")
            msg.setIcon(QMessageBox.Warning)
            msg.setInformativeText("Unable to connect to entered IP Address, please check connection to internet.")
            x = msg.exec_()
            return
        if self.clearPrevLogsChB.isChecked():
            print(check_output(["adb", "logcat", "-c"]))
            self.status.setText("Clearing Prev Logs")
        self.isLogging = True



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
