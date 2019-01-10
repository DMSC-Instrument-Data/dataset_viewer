from datasetviewer.mainview.interfaces.MainViewInterface import MainViewInterface
from datasetviewer.fileloader.FileLoaderWidget import FileLoaderWidget
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow

class MainWindow(MainViewInterface, QMainWindow):

    def __init__(self):

        QMainWindow.__init__(self)
        menubar = FileLoaderWidget(self)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle("Dataset Viewer")
        self.show()
        # uic.loadUi("datasetviewer/app/MainWindow.ui", self)

        # self.fname = "Not set..."
        # self.actionOpen.triggered.connect(self.open_file)
        # self.actionQuit.triggered.connect(self.close)

    def open_file(self):
        pass
        # filedialog = QFileDialog()
        # self.fname = filedialog.getOpenFileName(self, "Open file", "/home", "NetCDF (*.nc)")
        # notify ...
