from datasetviewer.preview.interfaces.PreviewPresenterInterface import PreviewPresenterInterface
from datasetviewer.mainview.interfaces.MainViewPresenterInterface import MainViewPresenterInterface
from datasetviewer.preview.Command import Command

class PreviewPresenter(PreviewPresenterInterface):
    """The subpresenter responsible for managing a PreviewView and providing it with the information that it will display.

    Args:
        preview_view (PreviewView): An instance of a PreviewView.

    Private Attributes:
        _view (PreviewView): The PreviewView containing interface elements that display a preview of the data. Assigned
            during initialisation.
        _data (DataSet): The data dictionary from which the preview is generated. Defaults to None. Is assigned once a
            file has been loaded by a user.

        Raises:
            ValueError: If the `preview_view` argument is None.

    """

    def __init__(self, preview_view):

        if preview_view is None:
            raise ValueError("Error: Cannot create PreviewPresenter when View is None.")

        self._view = preview_view
        self._data = None

    def set_data(self, dict):
        """Sets the `_data` attribute and calls a method to generate the preview contents.

        Args:
            dict (DataSet): The data dictionary.

        """
        self._data = dict
        self._populate_preview_list()

    def register_master(self, master):
        """

        Register the MainViewPresenter as the PreviewPresenter's master, and subscribe the MainViewPresenter to the
        PreviewPresenter.

        Args:
            master (MainViewPresenter): An instance of a MainViewPresenter.

        """
        assert (isinstance(master, MainViewPresenterInterface))

        self._main_presenter = master
        self._main_presenter.subscribe_preview_presenter(self)

    def _create_preview_text(self, name):
        """

        Generate the preview text that should appear for a given dictionary element. The preview consists of the
        name/key and its data dimensions.

        Args:
            name (str): The name/key associated with an element of the DataSet.

        """

        var = self._data[name]
        dims = var.get_dimensions()

        return name + "\n" + str(dims)

    def _add_preview_entry(self, name):
        """

        Add the preview text consisting of a name/key and data dimensions to the PreviewView.

        Args:
            name (str): The name/key associated with a element of the DataSet.

        """

        entry_text = self._create_preview_text(name)
        self._view.add_entry_to_list(entry_text)

    def _populate_preview_list(self):
        """ Fill the preview pane with the information about all of the elements in the DataSet. """
        for key, _ in self._data.items():
            self._add_preview_entry(key)

    def notify(self, command):

        if command == Command.ELEMENTSELECTION:

            selection = self._view.get_selected_item()

            # Trim the dimension information from the string
            key = selection.text().split("\n")[0]
