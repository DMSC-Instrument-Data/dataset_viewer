from datasetviewer.plot.interfaces.PlotPresenterInterface import PlotPresenterInterface

class PlotPresenter(PlotPresenterInterface):

    def __init__(self, view):

        self._view = view
        self._data = None

        # Define a fixed plot colour so that it doesn't change every time a slider is moved
        self.fixed_color = 'green'

    def create_default_plot(self, data):

        self.clear_plot()
        self._data = data

        if data.ndim == 1:
            self._view.ax.plot(data)

        elif data.ndim == 2:
            self._view.ax.plot(data[0])

        else:

            # selection = {}
            # count = 0

            for dim in data.dims:
                pass

    def create_onedim_plot(self):
        pass

    def create_twodim_plot(self):
        pass

    def clear_plot(self):
        pass

    def register_master(self, master):
        pass
