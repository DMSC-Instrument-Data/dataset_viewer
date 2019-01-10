from datasetviewer.mainview.interfaces.MainViewInterface import MainViewInterface
from datasetviewer.mainview.MainViewPresenter import MainViewPresenter
from datasetviewer.fileloader.FileLoaderWidget import FileLoaderWidget
from PyQt5.QtWidgets import QMainWindow, QAction

class MainWindow(MainViewInterface, QMainWindow):

    def __init__(self):

        QMainWindow.__init__(self)

        menubar = self.menuBar()
        filemenu = menubar.addMenu("File")

        fileloaderwidget = FileLoaderWidget(self)
        filemenu.addAction(fileloaderwidget)

        # Action for exiting the program
        exitAct = QAction("Exit", self)
        exitAct.triggered.connect(self.close)
        filemenu.addAction(exitAct)

        fileloaderpresenter = fileloaderwidget.get_presenter()

        # also add preview presenter to arguments
        mainviewpresenter = MainViewPresenter(self,fileloaderpresenter)

        self.statusBar()

        self.setGeometry(200, 200, 800, 600)
        self.setWindowTitle("Dataset Viewer")
        self.show()
