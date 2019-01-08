from datasetviewer.mainview.interfaces.MainViewInterface import MainViewInterface
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow

class MainWindow(MainViewInterface, QMainWindow):

    def __init__(self):

        QMainWindow.__init__(self)
        uic.loadUi("datasetviewer/app/MainWindow.ui", self)

        self.actionOpen.triggered.connect(self.test)

    def test(self):
        print("Pressed open button.")
