from datasetviewer.fileloader.interfaces.FileLoaderPresenterInterface import FileLoaderPresenterInterface
from datasetviewer.fileloader.Command import Command
import datasetviewer.fileloader.FileLoaderTool as FileLoaderTool
from datasetviewer.mainview.interfaces.MainViewPresenterInterface import MainViewPresenterInterface

class FileLoaderPresenter(FileLoaderPresenterInterface):
    """
    Presenter for overseeing the File Loading component of the interface. Receives commands from an associated
    FileLoaderView via a `notify` method. If a `FILEOPENREQUEST` signal is received then the FileLoaderPresenter
    attempts to open this file and pass the data to the MainViewPresenter.

    Private Attributes:
        _main_presenter (MainViewPresenter): The MainViewPresenter object. This is set to None in the constructor and
            assigned with the `register_master` method.
        _view (FileLoaderView): The FileLoaderView that this Presenter will manage.

    Raises:
        ValueError: If the `file_loader_view` is None.
    """

    def __init__(self, file_loader_view):

        super().__init__()

        if file_loader_view is None:
            raise ValueError("Error: Cannot create FileLoaderPresenter when View is None.")

        self._main_presenter = None
        self._view = file_loader_view

    def register_master(self, master):
        """
        Register the MainViewPresenter as the FileLoaderPresenter's master. The MainViewPresenter doesn't have a
        `subscribe_file_loader_presenter` method as it doesn't send instructions to the FileLoaderPresenter, so it
        doesn't need to store a reference to it.

        Args:
            master (MainViewPresenter): An instance of a MainViewPresenter.
        """

        assert (isinstance(master, MainViewPresenterInterface))

        self._main_presenter = master

    def notify(self, command):
        """
        Interpret a command from the FileLoaderView and take the appropriate action.

        Note:
            `register_master` must be called before this method can be called.

        Args:
            command (Command): A Command from the FileLoaderView indicating that an event has taken place.

        Raises:
            ValueError: If the command isn't recognised.
        """

        if command == Command.FILEOPENREQUEST:
            file_path = self._view.get_selected_file_path()[0]

            # Do nothing if the FileDialog was closed without a file being selected
            if not file_path:
                return

            try:
                dict = self._load_data(file_path)
                self._main_presenter.set_dict(dict)

            # Instruct the view to show a message if a valid filename was given but the file is invalid
            except (ValueError, OSError) as e:
                self._view.show_reject_file_message(str(e))

        else:
            raise ValueError("FileLoaderPresenter received an unrecognised command: {}".format(str(command)))

    def _load_data(self, file_path):
        """
        Given a file path, load this file and covert it to a data dictionary. Instructs the view to display a message
        indicating that the file could not be loaded in the case of failure.

        Args:
            file_path (str): The path of the file to be loaded.

        Returns:
            DataSet: An OrderedDict of Variables containing xarrays.

        Raises:
            ValueError: If the file does not exist.
            OSError: If the file exists, but does not have the appropriate format/contents and cannot be converted to
                an xarray.
        """

        dict = FileLoaderTool.file_to_dict(file_path)
        return dict
