from datasetviewer.plot.interfaces.PlotPresenterInterface import PlotPresenterInterface
from datasetviewer.mainview.interfaces.MainViewPresenterInterface import MainViewPresenterInterface

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
            self._view.plot_line(data)

        elif data.ndim == 2:
            self._view.plot_line(data[0])

        else:
            self._view.plot_image(data.isel({dim:0 for dim in data.dims[2:]})
                                      .transpose(data.dims[1],data.dims[0]))

    def clear_plot(self):

        # Try to delete a line plot if it exists
        try:
            self._view.line.pop(0).remove()
        except Exception:
            # Exception - plot being displayed is a colourmap
            pass

        # Prevent next plot from taking shape of the previous plot
        try:
            self._view.ax.cla()
        except Exception:
            pass

        # Try to delete a colourbar if it exists
        try:
            self._view.cbar.remove()
        except Exception:
            pass

        # Try to delete a colormap if it exists
        try:
            self._view.im.remove()
        except Exception:
            pass

    def register_master(self, master):

        assert (isinstance(master, MainViewPresenterInterface))

        self._main_presenter = master
        master.subscribe_plot_presenter(self)
