from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from datasetviewer.plot.interfaces.PlotViewInterface import PlotViewInterface
from datasetviewer.plot.PlotPresenter import PlotPresenter
from matplotlib.figure import Figure

import matplotlib as mpl
mpl.rc('lines', color='blue')

class PlotWidget(FigureCanvasQTAgg, PlotViewInterface):

    def __init__(self):
        self.figure = Figure()
        self.ax = self.figure.add_subplot(1, 1, 1)
        FigureCanvasQTAgg.__init__(self, self.figure)

        self._presenter = PlotPresenter(self)

        self.line = None
        self.im = None
        self.cbar = None

    def plot_image(self, arr):

        self.im = self.ax.imshow(arr)
        self.cbar = self.figure.colorbar(self.im)
        self.draw()

    def plot_line(self, arr):

        self.line = self.ax.plot(arr)
        self.ax.set_aspect('auto')
        self.draw()

    def get_presenter(self):
        return self._presenter
