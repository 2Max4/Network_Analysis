from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget)
import os
import sys

class Screen(QDialog):
    def __init__(self, parent=None):
        super(Screen, self).__init__(parent)

        self.doPingTest = True
        self.doSpeedTest = True
        self.interval = 5
        self.ping_target = "www.google.de"
        self.threads = 1
        self.path = "./../Data"
        self.ping_file_name = "ping_test.csv"
        self.speed_test_file_name = "speed_test.csv"
        self.clear = False
        self.ping_file_path = os.path.join(self.path, self.ping_file_name)
        self.speed_test_file_path = os.path.join(self.path, self.speed_test_file_name)

        self.generateScreen()

    def createParameterLayout(self):
        pingTargetTextBox = QLineEdit(self.ping_target)
        pingIntervalSpinBox = QSpinBox()
        pingIntervalSpinBox.setValue(self.interval)
        pingResultFileNameTextBox = QLineEdit(self.ping_file_name)
        speedResultFileNameTextBox = QLineEdit(self.speed_test_file_name)
        clearOldResultCheckBox = QCheckBox("Clear Old Results?")
        clearOldResultCheckBox.setChecked(self.clear)

        parameterLayout = QFormLayout()
        parameterLayout.addRow("Ping Target: ", pingTargetTextBox)
        parameterLayout.addRow("Ping Interval: ", pingIntervalSpinBox)
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
        mainLayout.addLayout(testLayout, 6, 0, 1, 2)
        mainLayout.addLayout(actionButtonsLayout, 7, 0, 1, 2)
        self.setLayout(mainLayout)
        self.setWindowTitle("Network Test")
        QApplication.setStyle(QStyleFactory.create('Fusion'))

    def startTest(self):
        print("Test Started")

    def endTest(self):
        print("Test Ended")

    def generateGraph(self):
        print("Generate Graph Started")

app = QApplication(sys.argv)
screen = Screen()
screen.show()
sys.exit(app.exec_())
