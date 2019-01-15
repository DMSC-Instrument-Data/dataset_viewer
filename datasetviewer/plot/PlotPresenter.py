from datasetviewer.plot.interfaces.PlotPresenterInterface import PlotPresenterInterface

class PlotPresenter(PlotPresenterInterface):

    def __init__(self, view):

        self._view = view
        self._data = None
        self.n_dims = 0

        # Define a fixed plot colour so that it doesn't change every time a slider is moved
        self.fixed_color = 'green'

    def create_default_plot(self, data):

        self.clear_plot()
        self._data = data

        self.n_dims = len(data.shape)


        if self.n_dims == 1:
            self._view.ax.plot(data, color=self.fixed_color)
        elif self.n_dims == 2:
            self._view.ax.plot(self.create_onedim_plot(), color=self.fixed_color)
        else:
            self.create_twodim_plot()

    def create_onedim_plot(self):
        pass

    def create_twodim_plot(self):
        pass

    def clear_plot(self):
        pass

    def register_master(self, master):
        pass
