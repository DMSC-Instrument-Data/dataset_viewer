from datasetviewer.fileloader.interfaces.FileLoaderViewInterface import FileLoaderViewInterface
from PyQt5.QtWidgets import QWidget, QMenuBar, QGridLayout

class FileLoaderWidget(FileLoaderViewInterface, QWidget):

    def __init__(self, parent = None):

        self.menu_bar = QMenuBar(self).addMenu("Open File")

        self.action = self.menu_bar.addAction("Open File")
        # self.action.triggered.connect(self.load_file)

        layout = QGridLayout(self)
        layout.addWidget(self.menu_bar, 0, 0)

    def load_file(self):
        print("Loading a file...")
