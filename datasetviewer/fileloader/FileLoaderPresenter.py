from datasetviewer.presenter.SubPresenter import SubPresenter
from datasetviewer.fileloader.Command import Command
from datasetviewer.fileloader.FileLoaderTool import FileLoaderTool
from datasetviewer.mainview.interfaces.MainViewPresenterInterface import MainViewPresenterInterface


class FileLoaderPresenter(SubPresenter):

    def __init__(self, file_loader_view):

        super().__init__()

        if file_loader_view is None:
            raise ValueError("Error: Cannot create FileLoaderPresenter when View is None.")

        self._main_presenter = None
        self._view = file_loader_view
        self._file_reader = FileLoaderTool()

    def register_master(self, master):

        assert (isinstance(master, MainViewPresenterInterface))

        # Register master must be called a subpresenter can call notify on the main presenter
        self._main_presenter = master
        self._main_presenter.subscribe_subpresenter(self)

    def notify(self, command):

        if command == Command.FILEOPENREQUEST:
            file_path = self._view.get_selected_file_path()
            dict = self.load_data(file_path)
            self._main_presenter.set_data(dict)

        else:
            raise ValueError("FileLoaderPresenter received an unrecognised command: {}".format(str(command)))

    def load_data(self, file_path):

        try:
            dict = self._file_reader.file_to_dict(file_path)
            return dict

        except (ValueError, TypeError) as e:
            self._view.show_reject_file_message(str(e))
