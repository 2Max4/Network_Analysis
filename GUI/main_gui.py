from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget)

class Screen(QDialog):
    def __init__(self, parent=None):
        super(Screen, self).__init__(parent)
        self.main_screen = QApplication.palette()
        self.doPingTest = True
        self.doSpeedTest = True
        self.generateScreen()

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
        mainLayout = QGridLayout()
        mainLayout.addLayout(testLayout, 0, 0, 1, 2)
        mainLayout.addLayout(actionButtonsLayout, 1, 0, 1, 2)
        self.setLayout(mainLayout)
        self.setWindowTitle("Network Test")
        QApplication.setStyle(QStyleFactory.create('Fusion'))

    def startTest(self):
        print("Test Started")

    def endTest(self):
        print("Test Ended")

    def generateGraphButton(self):
        print("Generate Graph Started")

import sys
app = QApplication(sys.argv)
screen = Screen()
screen.show()
sys.exit(app.exec_())
