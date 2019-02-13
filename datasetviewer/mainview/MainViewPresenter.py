from datasetviewer.mainview.interfaces.MainViewPresenterInterface import MainViewPresenterInterface

class MainViewPresenter(MainViewPresenterInterface):
    """
    MainViewPresenter that controls SubPresenters and calls their `register_master` method during initialisation. Also
    controls the MainView by updating its toolbar.

    Args:
        mainview (MainView): Instance of a MainView.
        subpresenters: One or more SubPresenters.

    Private Attributes:
        _main_view (MainView): MainView associated with this Presenter.
        _preview_presenter (PreviewPresenter): The Presenter that handles the behaviour of the PreviewView.
            Defaults to None.
        _plot_presenter (PlotPresenter): The Presenter that handles the behaviour of the PlotView. Defaults to None.
        _file_loader_presenter (FileLoaderPresenter): The presenter that handles the behaviour of the FileLoaderView.
            Defaults to None.
        _stack_presenter (StackPresenter): The Presenter that places DimensionView objects in different layers and
            changes the visible layer depending on which dictionary element has been selected. Defaults to None.
        _dict (DataSet): An OrderedDict of Variables. Defaults to None.

    Raises:
        ValueError: If the MainView or any of the SubPresenters are None.
    """

    def __init__(self, mainview, *subpresenters):

        if mainview is None:
            raise ValueError("Error: Cannot create MainViewPresenter when MainView is None.")

        self._main_view = mainview
        self._preview_presenter = None
        self._plot_presenter = None
        self._file_loader_presenter = None
        self._stack_presenter = None
        self._dict = None

        for presenter in subpresenters:

            if presenter is None:
                raise ValueError("Error: Cannot create MainViewPresenter when a SubPresenter is None.")

            presenter.register_master(self)

    def set_dict(self, dict):
        """
        Sets the `_dict` attribute in the MainViewPresenter and other Presenters that require access to the data
        dictionary.

        Note:
            The PlotPresenter, StackPresenter, and PreviewPresenter must be registered with master before this method is
            called.

        Args:
            dict (DataSet): The data dictionary.
        """

        self._dict = dict
        self._plot_presenter.set_dict(dict)
        self._stack_presenter.set_dict(dict)
        self._preview_presenter.set_dict(dict)

    def subscribe_preview_presenter(self, prev):
        """
        Sets the preview_presenter attribute so that it can be controlled when a file has been loaded.

        Args:
            prev (PreviewPresenter): An instance of a PreviewPresenter.
        """

        self._preview_presenter = prev

    def subscribe_plot_presenter(self, plot):
        """
        Sets the plot_presenter attribute so that it can be controlled when a file has been loaded or the plot is
        altered.

        Args:
            plot (PlotPresenter): An instance of a PlotPresenter.
        """

        self._plot_presenter = plot

    def subscribe_stack_presenter(self, stack):
        """
        Sets the stack_presenter attribute so that it can be controlled when a file has been loaded or the preview
        selection changes.

        Args:
            stack (StackPresenter): An instance of a StackPresenter.
        """

        self._stack_presenter = stack

    def change_current_key(self, key):
        """
        Tells the PlotPresenter to create the default plot of the current dataset, and tells the StackPresenter to
        change its visible layer.

        Args:
            key (str): The key of the dictionary element to be plotted.
        """

        self._plot_presenter.change_current_key(key)
        self._stack_presenter.change_current_key(key)

    def update_toolbar(self):
        """ Calls the `update_toolbar` function in the MainWindow so that the "Home" button works works correctly. """

        self._main_view.update_toolbar()

    def create_onedim_plot(self, key, x_dim, slice):
        """
        Instructs the PlotPresenter to create a 1D plot.

        Args:
            key (str): The key of the dataset to plot.
            x_dim (str): The name of the dimension that should be used for the x-axis.
            slice (dict): A dictionary of dimension-name/int pairs that indicate how the remaining dimensions should be
                sliced in the 1D plot.
        """

        self._plot_presenter.create_onedim_plot(key, x_dim, slice)

    def create_twodim_plot(self, key, x_dim, y_dim, slice):
        """
        Instructs the PlotPresenter to create a 2D plot.

        Args:
            key (str): The key of the dataset to plot.
            x_dim (str): The name of the dimension that should be used for the x-axis.
            y_dim (str): The name of the dimension that should be used for the y-axis.
            slice (dict): A dictionary of dimension-name/int pairs that indicate how the remaining dimensions should be
                sliced in the 2D plot.
        """

        self._plot_presenter.create_twodim_plot(key, x_dim, y_dim, slice)
