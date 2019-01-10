from datasetviewer.mainview.interfaces.MainViewInterface import MainViewInterface
from datasetviewer.mainview.MainViewPresenter import MainViewPresenter
from datasetviewer.fileloader.FileLoaderWidget import FileLoaderWidget
from datasetviewer.preview.PreviewWidget import PreviewWidget
from PyQt5.QtWidgets import QMainWindow, QAction, QGridLayout, QWidget

class MainWindow(MainViewInterface, QMainWindow):

    def __init__(self):

        QMainWindow.__init__(self)

        menubar = self.menuBar()
        filemenu = menubar.addMenu("File")

        file_loader_widget = FileLoaderWidget(self)
        filemenu.addAction(file_loader_widget)

        # Action for exiting the program
        exitAct = QAction("Exit", self)
        exitAct.triggered.connect(self.close)
        filemenu.addAction(exitAct)

        preview_widget = PreviewWidget()
        preview_presenter = preview_widget.get_presenter()

        file_loader_presenter = file_loader_widget.get_presenter()

        main_view_presenter = MainViewPresenter(self,file_loader_presenter, preview_presenter)

        self.statusBar()

        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        gridLayout = QGridLayout(self)
        centralWidget.setLayout(gridLayout)

        gridLayout.addWidget(preview_widget, 0, 0)

        self.show()
