from PyQt5.QtCore import pyqtSignal, QObject
def initializeGlobalVars():
    global runningTest
    runningTest = False

class Communicate(QObject):
    GUI_signal = pyqtSignal(str)
