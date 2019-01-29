from datasetviewer.plot.interfaces.PlotPresenterInterface import PlotPresenterInterface
from datasetviewer.mainview.interfaces.MainViewPresenterInterface import MainViewPresenterInterface

class PlotPresenter(PlotPresenterInterface):
    """The subpresenter responsible for managing a PlotView and creating the arrays for it to plot.

    Args:
        plot_view (PreviewView): An instance of a PlotView.

    Private Attributes:
        _view (PlotView): The PlotView containing the interface elements that display a plot. Assigned
            during initialisation.
        _dict (DataSet): An OrderedDict of xarray Datasets. Defaults to None.

        Raises:
            ValueError: If the `plot_view` argument is None.
    """

    def __init__(self, plot_view):

        if plot_view is None:
            raise ValueError("Error: Cannot create PlotPresenter when View is None.")

        self._view = plot_view
        self._dict = None

    def set_dict(self, dict):
        """ Set the `_dict` variable to an OrderedDict and plot the first element in the dictionary.

        Args:
            dict (DataSet): An OrderedDict of xarray Datasets.
        """

        self._dict = dict
        self.create_default_plot(list(dict.keys())[0])

    def create_default_plot(self, key):
        """Creates a default plot for different data types depending on the number of dimensions.

        Args:
            key (str): A key corresponding with the element to be plotted.
        """

        # Clear a previous plot if one exists
        self._clear_plot()

        data = self._dict[key].data

        if data.ndim == 1:
            # If the array is 1D then plot it as it is
            self._view.plot_line(data)

        elif data.ndim == 2:

            # Slice the array if it is 2D, then create a 1D plot with the first dimension as the X axis
            self._view.plot_line(data.transpose()[0])

            self._view.label_x_axis(data.dims[0])

        else:

            # Slice the array by using the first two dimensions as the X and Y axes if it is 2D or greater
            self._view.plot_image(data.isel({dim:0 for dim in data.dims[2:]})
                                      .transpose(data.dims[1],data.dims[0]))

            self._view.label_x_axis(data.dims[0])
            self._view.label_y_axis(data.dims[1])

        self._draw_plot()

        # Update the toolbar so that it returns to this plot when the "Home" button is pressed
        self._main_presenter.update_toolbar()

    def _clear_plot(self):
        """ Erases the previous plot and plot elements if they exist. """

        # Try to delete a line plot if it exists
        try:
            self._view.line.pop(0).remove()
        except Exception:
            pass

        # Prevent next plot from taking shape of the previous plot by clearing the axis
        try:
            self._view.ax.cla()
        except Exception:
            pass

        # Try to delete a colourbar if it exists
        try:
            self._view.cbar.remove()
        except Exception:
            pass

        # Try to delete a 2D plot if it exists
        try:
            self._view.im.remove()
        except Exception:
            pass

    def _draw_plot(self):
        """ Redraw the plot in the view after an update has occurred."""
        self._view.draw_plot()

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

    def create_onedim_plot(self, key, x_dim, slice):

        self._clear_plot()
        data = self._dict[key].data
        self._view.plot_line(data.isel(slice))
        self._view.label_x_axis(x_dim)
        self._draw_plot()

    def create_twodim_plot(self, key, x_dim, y_dim, slice):

        self._clear_plot()
        data = self._dict[key].data
        self._view.plot_image(data.isel(slice).transpose(y_dim, x_dim))
        self._view.label_x_axis(x_dim)
        self._view.label_y_axis(y_dim)
        self._draw_plot()
