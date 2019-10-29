from PyQt5.QtCore import QDateTime, Qt, QTimer, pyqtSignal, QObject

from PyQt5.QtWidgets import (QDialog, QApplication, QLabel, QCheckBox, QHBoxLayout,
                            QPushButton, QLineEdit, QSpinBox, QFormLayout, QGridLayout,
                            QStyleFactory)
import os
import sys
import json
import time
import threading

import modules.Communicate as Communicate

Communicate.initializeGlobalVars()

from modules.NetworkTest import NetworkTest as ntc

FilePath = "./defaults.json"



class Test:
    def __init__(self, callbackFunc):
        self.src = Communicate()
        self.src.GUI_signal.connect(callbackFunc)

    def runTest(self):
        global runningTest
        while(True):
            if(runningTest):
                print(time.time())
                msgForGui = 'Test is running'
                self.src.GUI_signal.emit(msgForGui)
            else:
                print("Test is stopped")
            time.sleep(1.5)

def loadDefaults(FilePath):
    with open(FilePath) as data:
        defaults = json.load(data)
    return defaults

class Screen(QDialog):
    def __init__(self, defaults, parent=None):
        super(Screen, self).__init__(parent)

        self.doPingTest = defaults["doPingTest"]
        self.doSpeedTest = defaults["doSpeedTest"]
        self.interval = defaults["interval"]
        self.ping_target = defaults["ping_target"]
        self.threads = defaults["threads"]
        self.path = defaults["path"]
        self.ping_file_name = defaults["ping_file_name"]
        self.speed_test_file_name = defaults["speed_test_file_name"]
        self.clear = defaults["clear"]

        self.test = ntc(defaults, self.testCallback)
        self.testThread = threading.Thread(name = 'runTest',
                                            target = self.test.run_network_test,
                                            args = (self.doPingTest, self.doSpeedTest)
                                    )
        self.testThread.daemon = True
        self.testThread.start()
        self.generateScreen()

    def createParameterLayout(self):
        pingTargetTextBox = QLineEdit(self.ping_target)
        pingIntervalSpinBox = QSpinBox()
        pingIntervalSpinBox.setValue(self.interval)
        resultFilePathTextBox = QLineEdit(self.path)
        pingResultFileNameTextBox = QLineEdit(self.ping_file_name)
        speedResultFileNameTextBox = QLineEdit(self.speed_test_file_name)
        clearOldResultCheckBox = QCheckBox("Clear Old Results?")
        clearOldResultCheckBox.setChecked(self.clear)

        parameterLayout = QFormLayout()
        parameterLayout.addRow("Ping Target: ", pingTargetTextBox)
        parameterLayout.addRow("Ping Interval: ", pingIntervalSpinBox)
        parameterLayout.addRow("Results File Path: ", resultFilePathTextBox)
        parameterLayout.addRow("Ping Test Result File Name: ", pingResultFileNameTextBox)
        parameterLayout.addRow("Speed Test Result File Name: ", speedResultFileNameTextBox)
        parameterLayout.addRow(clearOldResultCheckBox)
        return parameterLayout

    def createTestLayout(self):
        testLabel = QLabel("Select the test you want to perform: ")
        pingTestCheckbox = QCheckBox("&Ping Test")
        pingTestCheckbox.setChecked(self.doPingTest)
        speedTestCheckbox = QCheckBox("&Speed Test")
        speedTestCheckbox.setChecked(self.doSpeedTest)

        testLayout = QHBoxLayout()
        testLayout.addWidget(testLabel)
        testLayout.addWidget(pingTestCheckbox)
        testLayout.addWidget(speedTestCheckbox)
        return testLayout

    def creatActionButtonsLayout(self):
        startTestButton = QPushButton("Start Test")
        startTestButton.clicked.connect(self.startTest)
        endTestButton = QPushButton("End Test")
        endTestButton.clicked.connect(self.endTest)
        generateGraphButton = QPushButton("Generate Graph")
        generateGraphButton.clicked.connect(self.generateGraph)

        actionButtonsLayout = QHBoxLayout()
        actionButtonsLayout.addWidget(startTestButton)
        actionButtonsLayout.addWidget(endTestButton)
        actionButtonsLayout.addWidget(generateGraphButton)
        return actionButtonsLayout

    def generateScreen(self):
        testLayout = self.createTestLayout()
        actionButtonsLayout = self.creatActionButtonsLayout()
        parameterLayout = self.createParameterLayout()

        mainLayout = QGridLayout()
        mainLayout.addLayout(parameterLayout, 0, 0, 5, 2)
        mainLayout.addLayout(testLayout, 7, 0, 1, 2)
        mainLayout.addLayout(actionButtonsLayout, 8, 0, 1, 2)
        self.setLayout(mainLayout)
        self.setWindowTitle("Network Test")
        QApplication.setStyle(QStyleFactory.create('Fusion'))

    def startTest(self):
        print("Test Started")
        Communicate.runningTest = True


    def endTest(self):
        Communicate.runningTest = False
        print("Test Ended")

    def generateGraph(self):
        print("Generate Graph Started")

    def testCallback(self, msg):
        # print('the thread has sent this message to the GUI:')
        global runningTest
        print(msg)

app = QApplication(sys.argv)
screen = Screen(loadDefaults(FilePath))
screen.show()
sys.exit(app.exec_())
