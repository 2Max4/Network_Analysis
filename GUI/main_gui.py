from tkinter import *

class Screen:
    def __init__(self):
        self.main_screen = Tk()
        self.doPingTest = IntVar()
        self.doSpeedTest = IntVar()

    def createTest(self):
        Label(self.main_screen, text="Select the test you want to perform.").grid(row=0, sticky=W)
        Checkbutton(self.main_screen, text="Ping Test", variable=self.doPingTest).grid(row=1, sticky=W)
        Checkbutton(self.main_screen, text="Speed Test", variable=self.doSpeedTest).grid(row=2, sticky=W)
        Button(text = "Start Test", command = self.startTest).grid(row=3, sticky=W)
        Button(text = "End Test", command = self.endTest).grid(row=3, column=1, sticky=W)

    def printVar(self):
        print(self.doPingTest.get(), self.doSpeedTest.get())

    def startTest(self):
        print("Test Started")

    def endTest(self):
        print("Test Ended")

    def display(self):
        self.main_screen.mainloop()

screen = Screen()
screen.createTest()
screen.display()
