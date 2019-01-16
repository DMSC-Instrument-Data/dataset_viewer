from datasetviewer.plot.interfaces.PlotPresenterInterface import PlotPresenterInterface
from datasetviewer.mainview.interfaces.MainViewPresenterInterface import MainViewPresenterInterface

class PlotPresenter(PlotPresenterInterface):
    """The subpresenter responsible for managing a PlotView and creating the arrays for it to plot.

    Args:
        plot_view (PreviewView): An instance of a PlotView.

    Private Attributes:
        _view (PlotView): The PlotView containing the interface elements that display a plot. Assigned
            during initialisation.
        _data (DataArray): A data dictionary element that is plotted. Defaults to None. Is assigned once a
            file has been loaded by a user.

        Raises:
            ValueError: If the `plot_view` argument is None.
    """

    def __init__(self, plot_view):

        if plot_view is None:
            raise ValueError("Error: Cannot create PlotPresenter when View is None.")

        self._view = plot_view
        self._data = None

    def create_default_plot(self, data):
        """Creates a default plot for different data types depending on the number of dimensions.

        Args:
            data (DataArray): An xarray dataset containing nD data.
        """

        # Clear a previous plot if one exists
        self.clear_plot()

        self._data = data

        if data.ndim == 1:
            # Plot the array as it is if it is 1D
            self._view.plot_line(data)

        elif data.ndim == 2:

            # Slice the array if it is 2D, then create a 1D plot
            self._view.plot_line(data.transpose()[0])

            self._view.label_x_axis(data.dims[0])

        else:

            # Slice the array by using the first two dimensions as the X and Y axes if it is 2D or greater
            self._view.plot_image(data.isel({dim:0 for dim in data.dims[2:]})
                                      .transpose(data.dims[1],data.dims[0]))

            self._view.label_x_axis(data.dims[0])
            self._view.label_y_axis(data.dims[1])

        self._view.draw_plot()
        self._main_presenter.update_toolbar()

    def clear_plot(self):
        """ Erases the previous plot and plot elements if they exist. """

        # Try to delete a line plot if it exists
        try:
            self._view.line.pop(0).remove()
        except Exception:
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
        """

        Register the MainViewPresenter as the PlotPresenter's master, and subscribe the MainViewPresenter to the
        PlotPresenter.

        Args:
            master (MainViewPresenter): An instance of a MainViewPresenter.

        """

        assert (isinstance(master, MainViewPresenterInterface))

        self._main_presenter = master
        master.subscribe_plot_presenter(self)
