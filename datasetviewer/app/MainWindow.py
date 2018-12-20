from datasetviewer.mainview.interfaces.MainViewInterface import MainViewInterface
from PyQt5.QtWidgets import QMainWindow

class MainWindow(MainViewInterface, QMainWindow):

    def __init__(self):

        QMainWindow.__init__(self)
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Dataset Viewer')
        self.show()
