from matplotlib.backends.backend_qt5agg import FigureCanvas
from datasetviewer.plot.interfaces.PlotViewInterface import PlotViewInterface

import matplotlib as mpl
mpl.rc('lines', color='blue')

class PlotView(FigureCanvas, PlotViewInterface):

    def plot_image(self, arr):
        pass

    def plot_line(self, arr):
        pass
