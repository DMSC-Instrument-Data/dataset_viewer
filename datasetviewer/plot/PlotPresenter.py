from datasetviewer.plot.interfaces.PlotPresenterInterface import PlotPresenterInterface

class PlotPresenter(PlotPresenterInterface):

    def __init__(self, view):

        self._plot_view = view
        self._data = None

    def create_default_plot(self, data):

        self.clear_plot()
        self._data = data

    def clear_plot(self):
        pass

    def register_master(self, master):
        pass
