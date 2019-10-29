from PyQt5.QtCore import QDateTime, Qt, QTimer, pyqtSignal, QObject

from PyQt5.QtWidgets import (QDialog, QApplication, QLabel, QCheckBox, QHBoxLayout, QVBoxLayout,
                            QPushButton, QLineEdit, QSpinBox, QFormLayout, QGridLayout,
                            QStyleFactory)
import os
import sys
import json
import time
import threading
import webbrowser

from modules.NetworkTest import NetworkTest as ntc

FilePath = "./defaults.json"

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
                                            args = ()
                                    )
        self.testThread.daemon = True
        self.testThread.start()
        self.generateScreen()

    def createParameterLayout(self):
        self.pingTargetTextBox = QLineEdit(self.ping_target)
        self.pingIntervalSpinBox = QSpinBox()
        self.pingIntervalSpinBox.setValue(self.interval)
        self.threadsSpinBox = QSpinBox()
        self.threadsSpinBox.setValue(self.threads)
        self.resultFilePathTextBox = QLineEdit(self.path)
        self.pingResultFileNameTextBox = QLineEdit(self.ping_file_name)
        self.speedResultFileNameTextBox = QLineEdit(self.speed_test_file_name)
        self.clearOldResultCheckBox = QCheckBox("Clear Old Results?")
        self.clearOldResultCheckBox.setChecked(self.clear)

        parameterLayout = QFormLayout()
        parameterLayout.addRow("Ping Target: ", self.pingTargetTextBox)
        parameterLayout.addRow("Ping Interval: ", self.pingIntervalSpinBox)
        parameterLayout.addRow("Threads to use: ", self.threadsSpinBox)
        parameterLayout.addRow("Results File Path: ", self.resultFilePathTextBox)
        parameterLayout.addRow("Ping Test Result File Name: ", self.pingResultFileNameTextBox)
        parameterLayout.addRow("Speed Test Result File Name: ", self.speedResultFileNameTextBox)
        parameterLayout.addRow(self.clearOldResultCheckBox)
        return parameterLayout

    def createTestLayout(self):
        testLabel = QLabel("Select the test you want to perform: ")
        self.pingTestCheckbox = QCheckBox("&Ping Test")
        self.pingTestCheckbox.setChecked(self.doPingTest)
        self.speedTestCheckbox = QCheckBox("&Speed Test")
        self.speedTestCheckbox.setChecked(self.doSpeedTest)

        testLayout = QHBoxLayout()
        testLayout.addWidget(testLabel)
        testLayout.addWidget(self.pingTestCheckbox)
        testLayout.addWidget(self.speedTestCheckbox)
        return testLayout

    def creatActionButtonsLayout(self):
        startTestButton = QPushButton("Start Test")
        startTestButton.clicked.connect(self.startTest)
        endTestButton = QPushButton("End Test")
        endTestButton.clicked.connect(self.endTest)


        actionButtonsLayout = QHBoxLayout()
        actionButtonsLayout.addWidget(startTestButton)
        actionButtonsLayout.addWidget(endTestButton)
        return actionButtonsLayout

    def createRightActionPanel(self):
        generateGraphButton = QPushButton("Generate Graph")
        generateGraphButton.clicked.connect(self.generateGraph)
        viewGraphButton = QPushButton("View Graph")
        viewGraphButton.clicked.connect(self.viewGraph)

        rightActionLayout = QVBoxLayout()
        rightActionLayout.addWidget(generateGraphButton)
        rightActionLayout.addWidget(viewGraphButton)
        return rightActionLayout

    def generateScreen(self):
        testLayout = self.createTestLayout()
        actionButtonsLayout = self.creatActionButtonsLayout()
        parameterLayout = self.createParameterLayout()
        rightActionLayout = self.createRightActionPanel()

        mainLayout = QGridLayout()
        mainLayout.addLayout(parameterLayout, 0, 0, 7, 2)
        mainLayout.addLayout(testLayout, 8, 0, 1, 2)
        mainLayout.addLayout(actionButtonsLayout, 9, 0, 1, 2)
        mainLayout.addLayout(rightActionLayout, 0, 2, 2, 1)

        self.setLayout(mainLayout)
        self.setWindowTitle("Network Test")
        QApplication.setStyle(QStyleFactory.create('Fusion'))

    def startTest(self):
        print("Test Started")
        self.doPingTest = self.pingTestCheckbox.isChecked()
        self.doSpeedTest = self.speedTestCheckbox.isChecked()
        self.interval = self.pingIntervalSpinBox.value()
        self.ping_target = self.pingTargetTextBox.text()
        self.threads = self.threadsSpinBox.value()
        self.path = self.resultFilePathTextBox.text()
        self.ping_file_name = self.pingResultFileNameTextBox.text()
        self.speed_test_file_name = self.speedResultFileNameTextBox.text()
        self.clear = self.clearOldResultCheckBox.isChecked()

        updatedVariables = {
            "doPingTest": self.doPingTest,
            "doSpeedTest": self.doSpeedTest,
            "interval": self.interval,
            "ping_target": self.ping_target,
            "threads": self.threads,
            "path": self.path,
            "ping_file_name": self.ping_file_name,
            "speed_test_file_name": self.speed_test_file_name,
            "clear": self.clear
        }
        self.test.updateTestVariables(updatedVariables)
        self.test.startTest()

    def endTest(self):
        self.test.endTest()
        print("Test Ended")

    def generateGraph(self):
        print("Generate Graph Started")
        self.test.generate_and_save_all_plots()

    def viewGraph(self):
        print("Opening Graph")
        webbrowser.open('file://' + os.path.realpath(os.path.join(self.path, "webpage", "index.html")))

    def testCallback(self, msg):
        # print(msg)
        pass

app = QApplication(sys.argv)
screen = Screen(loadDefaults(FilePath))
screen.show()
sys.exit(app.exec_())
