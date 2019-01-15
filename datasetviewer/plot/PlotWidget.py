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

    def plot_image(self, arr):
        self.ax.imshow(arr)
        self.draw()

    def plot_line(self, arr):
        self.ax.plot(arr)
        self.draw()

    def get_presenter(self):
        return self._presenter
