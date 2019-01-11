from datasetviewer.mainview.interfaces.MainViewPresenterInterface import MainViewPresenterInterface

class MainViewPresenter(MainViewPresenterInterface):
    """ MainViewPresenter that controls SubPresenters and calls their `register_master` method during initialisation.

    Args:
        mainview (MainView): Instance of a MainView.
        subpresenters (SubPresenter): One or more SubPresenters.

    Private Attributes:
        _main_view (MainView): MainView associated with this Presenter.
        _subpresenters (SubPresenter[]): A List of the associated SubPresenters.
        _preview_presenter (PreviewPresenter): The PreviewPresenter that handles the behaviour of the PreviewView.
            Defaults to None.
        -_data (DataSet): An OrderedDict of Variables. Defaults to None.

    Raises:
        ValueError: If the MainView or any of the SubPresenters are None.

    """

    def __init__(self, mainview, *subpresenters):

        if mainview is None:
            raise ValueError("Error: Cannot create MainViewPresenter when MainView is None.")

        self._main_view = mainview
        self._subpresenters = []
        self._preview_presenter = None
        self._data = None

        for presenter in subpresenters:

            if presenter is None:
                raise ValueError("Error: Cannot create MainViewPresenter when a SubPresenter is None.")

            presenter.register_master(self)

    def set_data(self, dict):
        """Sets the data attribute in the MainViewPresenter and other Presenters that require access to the data
            dictionary.

        Note:
            `subscribe_preview_presenter` must be called before this method can be called.

        Args:
            dict (DataSet): The data dictionary.

        """

        self._data = dict
        self._preview_presenter.set_data(dict)

    def subscribe_preview_presenter(self, prev):
        """Sets the preview_presenter attribute so that it can be controlled when a file has been loaded.

        Args:
            prev (PreviewPresenter): An instance of a PreviewPresenter.

        """
        self._preview_presenter = prev

    def subscribe_subpresenter(self, *subpresenter):
        """Appends the SubPresenter to the subpresenter list attribute.

        Args:
            subpresenter (SubPresenter): An instance of a SubPresenter.

        """

        self._subpresenters.append(subpresenter)

    def create_default_plot(self, key):
        pass
