from datasetviewer.mainview.interfaces.MainViewInterface import MainViewInterface
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QFileDialog

class MainWindow(MainViewInterface, QMainWindow):

    def __init__(self):

        QMainWindow.__init__(self)
        uic.loadUi("datasetviewer/app/MainWindow.ui", self)

        self.fname = "Not set..."
        self.actionOpen.triggered.connect(self.open_file)
        self.actionQuit.triggered.connect(self.close)

    def open_file(self):

        filedialog = QFileDialog()
        # filedialog.exec_()
        self.fname = filedialog.getOpenFileName(self, "Open file", "/home", "NetCDF (*.nc)")

        print(self.fname)
