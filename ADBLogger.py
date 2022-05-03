import os
import pathlib
import subprocess
import webbrowser
import multiprocessing
import psutil

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from pathvalidate import sanitize_filepath
from datetime import datetime
from PyQt5.QtCore import *
from qt_material import apply_stylesheet

fileName = ""
ipAddress = ""

class Ui_MainWindow(object):
    proc = multiprocessing.Process
    isLogging = False

    def __init__(self):
        self.t = None
        self.fileName = None
        self.ipAddress = None
        self.devices = []
        self.clearPrevLogs = None

    def setupUi(self, MainWindow):
        #####################################
        #           UI Components           #
        #####################################

        # Main Window
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(510, 265)
        MainWindow.setAutoFillBackground(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        apply_stylesheet(app, theme='dark_red.xml')

        # Start Button
        self.startBtn = QtWidgets.QPushButton(self.centralwidget)
        self.startBtn.setGeometry(QtCore.QRect(105, 112, 81, 31))
        self.startBtn.setObjectName("startBtn")
        self.startBtn.clicked.connect(self.startBtnClick)

        # IP Label
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 20, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")

        # IP Text Box
        self.ipAddressTB = QtWidgets.QLineEdit(self.centralwidget)
        self.ipAddressTB.setGeometry(QtCore.QRect(85, 15, 412, 35))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.ipAddressTB.setFont(font)
        self.ipAddressTB.setObjectName("ipAddressTB")

        # File Name Label
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 70, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

        # File Name TB
        self.fileNameTB = QtWidgets.QLineEdit(self.centralwidget)
        self.fileNameTB.setGeometry(QtCore.QRect(85, 65, 412, 35))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.fileNameTB.setFont(font)
        self.fileNameTB.setObjectName("fileNameTB")

        # Stop Button
        self.stopBtn = QtWidgets.QPushButton(self.centralwidget)
        self.stopBtn.setGeometry(QtCore.QRect(245, 112, 81, 31))
        self.stopBtn.setDisabled(True)
        self.stopBtn.setObjectName("stopBtn")
        self.stopBtn.clicked.connect(self.stopBtnClick)

        # Open Button
        self.openBtn = QtWidgets.QPushButton(self.centralwidget)
        self.openBtn.setGeometry(QtCore.QRect(395, 112, 81, 31))
        self.openBtn.setDisabled(True)
        self.openBtn.setObjectName("stopBtn")
        self.openBtn.clicked.connect(self.openBtnClick)

        # Status Label
        self.status = QtWidgets.QLabel(self.centralwidget)
        self.status.setGeometry(QtCore.QRect(85, 175, 412, 35))
        self.status.setText("")
        self.status.setAlignment(QtCore.Qt.AlignCenter)
        self.status.setObjectName("status")

        # Clear Prev Logs Check Box
        self.clearPrevLogsChB = QtWidgets.QCheckBox(self.centralwidget)
        self.clearPrevLogsChB.setGeometry(QtCore.QRect(85, 152, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.clearPrevLogsChB.setFont(font)
        self.clearPrevLogsChB.setObjectName("clearPrevLogsChB")

        # IP Address Combo Box
        self.ipAddressCB = QtWidgets.QComboBox(self.centralwidget)
        self.ipAddressCB.setGeometry(QtCore.QRect(85, 15, 412, 35))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.restoreSettings()
        self.ipAddressCB.setFont(font)
        self.ipAddressCB.setEditable(True)
        self.ipAddressCB.setVisible(False)
        self.ipAddressCB.setObjectName("ipAddressCB")

        # Progress Bar
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(85, 215, 412, 10))
        self.progressBar.setMaximum(0)
        self.progressBar.setProperty("value", -1)
        self.progressBar.setFormat("")
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setVisible(False)

        # Misc
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
        self.getAllDevices()

    def retranslateUi(self, MainWindow):
        # Set texts for Translations
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.startBtn.setText(_translate("MainWindow", "Start"))
        self.label.setText(_translate("MainWindow", "IP Address:"))
        self.ipAddressTB.setPlaceholderText(_translate("MainWindow", "IP Address"))
        self.label_2.setText(_translate("MainWindow", "File Name:"))
        self.fileNameTB.setPlaceholderText(_translate("MainWindow", "File Name"))
        self.stopBtn.setText(_translate("MainWindow", "Stop"))
        self.openBtn.setText(_translate("MainWindow", "Open"))
        self.clearPrevLogsChB.setText(_translate("MainWindow", "Clear Previous Logs"))
        self.ipAddressCB.setPlaceholderText(_translate("MainWindow", "IP Address"))

    def startBtnClick(self):
        # Pulls IP Address for validation
        if 1 == len(self.devices):
            self.ipAddress = self.ipAddressTB.text()
            if self.ipAddress not in self.devices:
                self.ipAddressCB.addItem(self.ipAddress)
                self.devices.append(self.ipAddress)
        elif len(self.devices) > 1:
            if self.ipAddress not in self.devices:
                self.ipAddressCB.addItem(self.ipAddress)
                self.devices.append(self.ipAddress)
                self.ipAddress = self.ipAddressCB.currentText()
        elif len(self.devices) == 0:
            self.ipAddress = self.ipAddressTB.text()
            self.devices.append(self.ipAddress)
        if self.ipAddress == "":
            msg = QMessageBox()
            msg.setWindowTitle("Invalid IP")
            msg.setText("Invalid IP entered, please try again!")
            msg.setIcon(QMessageBox.Warning)
            msg.setInformativeText("You have entered no information in the IP Address field, please enter IP Address.")
            x = msg.exec_()
            return
        # Pulls file name for validation and sanitization
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
        # Sets default file name if none provided
        if self.fileName == "":
            timeStamp = datetime.now()
            self.fileName = timeStamp.strftime("%d-%m-%Y-%H-%M-%S") + "-logs"
            self.fileName = sanitize_filepath(self.fileName)
            self.fileNameTB.setText(self.fileName)
            app.processEvents()
        # Disables start button and open button (stop is not enabled here due to the connect
            # command having inconsistent results when stopped).
        self.startBtn.setDisabled(True)
        self.openBtn.setDisabled(True)
        self.ipAddressTB.setDisabled(True)
        self.fileNameTB.setDisabled(True)
        self.ipAddressCB.setDisabled(True)
        self.status.setText("Attempting Connection...")
        app.processEvents()
        # Starts connection and validates connection.
        adbConnectionAttempt = str(os.system("adb connect "+self.ipAddress))
        if "failed" in adbConnectionAttempt:
            msg = QMessageBox()
            msg.setWindowTitle("Connection to IP Failed")
            msg.setText("Unable to connect to IP, please try again!")
            msg.setIcon(QMessageBox.Warning)
            msg.setInformativeText("Unable to connect to entered IP Address, please check connection to internet.")
            x = msg.exec_()
            self.stopBtnClick()
            return
        # Enables correct buttons and progress bar, clears previous logs if selected
        self.stopBtn.setDisabled(False)
        self.progressBar.setVisible(True)
        app.processEvents()
        self.clearPrevLog = self.clearPrevLogsChB.isChecked()
        if self.clearPrevLogs:
            self.status.setText("Clearing Prev Logs")
            app.processEvents()
            os.system("adb logcat -c")
        # Prepares for threading and logging.
        self.isLogging = True
        self.status.setText("Logging IP Address: " + self.ipAddress)
        self.t = TTT()
        self.t.fileName = self.fileName
        self.t.ipAddress = self.ipAddress
        self.t.start()

    def stopBtnClick(self):
        # Disables the progress bar, kills the adb process, ends logging and sets screen attributes
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
        self.openBtn.setDisabled(False)
        self.ipAddressTB.setDisabled(False)
        self.fileNameTB.setDisabled(False)
        self.ipAddressCB.setDisabled(False)

    def getAllDevices(self):
        proc = subprocess.Popen("adb devices", stdout=subprocess.PIPE)
        for index, line in enumerate(proc.stdout.readlines()):
            if str(":") in str(line):
                splitString = str(line.decode('unicode_escape')).split(str(":")[0])
                self.devices.append(splitString[0])
        print(self.devices)
        if self.devices:
            if len(self.devices) > 1:
                self.ipAddressTB.setVisible(False)
                self.ipAddressCB.setVisible(True)
                self.ipAddressCB.clear()
                self.ipAddressCB.addItems(self.devices)
                self.ipAddressCB.setCurrentIndex(0)
                app.processEvents()

    # Opens file path
    def openBtnClick(self):
        path = str(pathlib.Path().resolve())
        webbrowser.open('file:///' + path)

    # Close events will run the stop button method if closed incase logging.
    def closeEvent(self, event):
        self.stopBtnClick()
        super(Ui_MainWindow, self).closeEvent(event)

    # Saves previous user input
    def saveSettings(self):
        settings = QSettings('verizon', 'adblogger')
        settings.setValue('ipaddress', self.ipAddress)
        settings.setValue('devices', self.devices)
        settings.setValue('clearprevlogs', self.clearPrevLogs)

    # Pulls previous user input
    def restoreSettings(self):
        settings = QSettings('verizon', 'adblogger')
        self.ipAddress = settings.value('ipaddress', self.ipAddress)
        self.devices = settings.value('devices', self.devices)
        self.clearPrevLogs = settings.value('clearprevlogs', self.clearPrevLogs)
        if self.devices:
            if len(self.devices) == 1:
                self.ipAddressTB.setText(self.ipAddress)
            if len(self.devices) > 1:
                self.ipAddressCB.setCurrentText(self.ipAddress)
        self.clearPrevLogsChB.setChecked(bool(self.clearPrevLogs))

class TTT(QThread):
    def __init__(self):
        super(TTT, self).__init__()
        self.quit_flag = False
        self.fileName = ""
        self.ipAddress = ""

    def run(self):
        # Runs logcat
        if not self.quit_flag:
            os.system("adb -s " + self.ipAddress + " logcat > " + self.fileName + '.txt')
        self.quit()
        self.wait()


# Main Method
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
