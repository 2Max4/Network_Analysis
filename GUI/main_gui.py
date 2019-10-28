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
        speedTestCheckbox = QCheckBox("&Speed Test")
        testLayout = QHBoxLayout()
        testLayout.addWidget(testLabel)
        testLayout.addWidget(pingTestCheckbox)
        testLayout.addWidget(speedTestCheckbox)
        return testLayout

    def generateScreen(self):
        testLayout = self.createTestLayout()
        mainLayout = QGridLayout()
        mainLayout.addLayout(testLayout, 0, 0, 1, 2)
        self.setLayout(mainLayout)
        self.setWindowTitle("Network Test")
        QApplication.setStyle(QStyleFactory.create('Fusion'))

    def startTest(self):
        print("Test Started")

    def endTest(self):
        print("Test Ended")

    def display(self):
        pass

import sys
app = QApplication(sys.argv)
screen = Screen()
screen.show()
sys.exit(app.exec_())
