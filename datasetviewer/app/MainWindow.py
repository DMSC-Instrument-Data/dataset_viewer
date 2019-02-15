from datasetviewer.mainview.interfaces.MainViewInterface import MainViewInterface
from datasetviewer.mainview.MainViewPresenter import MainViewPresenter
from datasetviewer.fileloader.FileLoaderWidget import FileLoaderWidget
from datasetviewer.stack.StackWidget import StackWidget
from datasetviewer.dimension.DimensionViewFactory import DimensionViewFactory
from datasetviewer.preview.PreviewWidget import PreviewWidget
from PyQt5.QtWidgets import QMainWindow, QAction, QGridLayout, QWidget
from datasetviewer.plotting.PlotWidget import PlotWidget

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

class MainWindow(MainViewInterface, QMainWindow):

    def __init__(self, script_mode=False, dataset=None):

        QMainWindow.__init__(self)

        menubar = self.menuBar()
        filemenu = menubar.addMenu("File")

        subpresenters = []

        if not script_mode:
            # Don't add the File menu option if the viewer is being used in script mode
            file_loader_widget = FileLoaderWidget(self)
            subpresenters.append(file_loader_widget.get_presenter())
            filemenu.addAction(file_loader_widget)

        preview_widget = PreviewWidget()
        subpresenters.append(preview_widget.get_presenter())

        plot_widget = PlotWidget()
        subpresenters.append(plot_widget.get_presenter())
        self.toolbar = NavigationToolbar(plot_widget, self)
        self.addToolBar(self.toolbar)

        '''
        Create a DimensionViewFactory and pass this to the StackWidget. This enables it to create DimensionView objects
        when needed.
        '''
        dim_view_factory = DimensionViewFactory(self)
        stack_widget = StackWidget(dim_view_factory, self)
        subpresenters.append(stack_widget.get_presenter())

        if script_mode:
            MainViewPresenter(self, *subpresenters).set_dict(dataset)
        else:
            MainViewPresenter(self, *subpresenters)

        # Action for exiting the program
        exit_act = QAction("Exit", self)
        exit_act.triggered.connect(self.close)
        filemenu.addAction(exit_act)

        self.statusBar()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        grid_layout = QGridLayout()
        central_widget.setLayout(grid_layout)

        grid_layout.addWidget(preview_widget, 0, 0, 2, 1)
        grid_layout.addWidget(plot_widget, 0, 1, 1, 2)
        grid_layout.addWidget(stack_widget, 1, 1, 1, 2)

        self.setWindowTitle("Dataset Viewer")
        self.show()

    def update_toolbar(self):
        """ Informs the toolbar that the 'Home' button should take the plot back to the current state. Called when a new
            dataset is loaded. """

        self.toolbar.update()
        self.toolbar.push_current()
