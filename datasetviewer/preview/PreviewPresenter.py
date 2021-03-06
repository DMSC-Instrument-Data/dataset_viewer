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
        _dict (DataSet): The data dictionary from which the preview is generated. Defaults to None. Is assigned once a
            file has been loaded by a user. Defaults to None.

        Raises:
            ValueError: If the `preview_view` argument is None.

    """

    def __init__(self, preview_view):

        if preview_view is None:
            raise ValueError("Error: Cannot create PreviewPresenter when View is None.")

        self._view = preview_view
        self._dict = None

    def set_dict(self, dict):
        """Sets the `_data` attribute and then sets up a preview by clearing the previous contents, populating the list,
            and selecting the first item on the list.

        Args:
            dict (DataSet): An OrderedDict of xarray Datasets.

        """

        self._dict = dict
        self._view.clear_preview()
        self._view.reset_selection()
        self._populate_preview_list()
        self._view.select_first_item()

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
        name/key and its corresponding data dimensions.

        Args:
            name (str): The name/key associated with an element of the DataSet.

        Returns:
            str: A string containing the element key and its dimensions separated by a newline.

        """

        var = self._dict[name]
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
        for key in self._dict.keys():
            self._add_preview_entry(key)

    def notify(self, command):
        """

        Interpret a command from the PreviewView and take the appropriate action.

        Note:
            `register_master` must be called before this method can be called.

        Args:
            command (Command): A Command from the FileLoaderView indicating that an event has taken place.

        Raises:
            ValueError: If the command isn't recognised.

        """
        if command == Command.ELEMENTSELECTION:

            selection = self._view.get_selected_item()

            # Trim the dimension information from the string
            key = selection.text().split("\n")[0]

            self._main_presenter.create_default_plot(key)

        else:
            raise ValueError("PreviewPresenter received an unrecognised command: {}".format(str(command)))
