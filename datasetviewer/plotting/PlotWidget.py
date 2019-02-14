
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure

from datasetviewer.plotting.interfaces.PlotViewInterface import PlotViewInterface
from datasetviewer.plotting.PlotPresenter import PlotPresenter

class PlotWidget(FigureCanvas, PlotViewInterface):

    def __init__(self):

        self.figure = Figure()
        self.ax = self.figure.add_subplot(1, 1, 1)
        FigureCanvas.__init__(self, self.figure)

        # Create a PlotPresenter and give it a reference to the PlotView
        self._presenter = PlotPresenter(self)

        self.line = None
        self.im = None
        self.cbar = None

    def plot_image(self, arr):

        self.im = self.ax.imshow(arr)
        self.cbar = self.figure.colorbar(self.im)

    def plot_line(self, arr):

        self.line = self.ax.plot(arr)
        self.ax.set_aspect('auto')

    def draw_plot(self):
        self.draw()

    def get_presenter(self):
        return self._presenter

    def label_x_axis(self, label):
        self.ax.set_xlabel(label)

    def label_y_axis(self, label):
        self.ax.set_ylabel(label)
