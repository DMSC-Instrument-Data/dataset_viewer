from datasetviewer.fileloader.FileLoaderTool import FileLoaderTool
from datasetviewer.presenter.SubPresenter import SubPresenter
from datasetviewer.fileloader.Command import Command


class FileLoaderPresenter(SubPresenter):

    def __init__(self, data_set_source, preview_view):

        self._model = data_set_source
        self._main_presenter = None
        self._view = preview_view
        self._file_reader = FileLoaderTool()

    def register_master(self, master):

        self._main_presenter = master
        self._main_presenter.subscribe_subpresenter(self)

    def notify(self, command):

        if command == Command.FILEOPENREQUEST:
            file_path = self._view.get_selected_file_path()
            self.load_data_to_model(file_path)



    def load_data_to_model(self, file_path):

        try:
            dict = self._file_reader.file_to_dict(file_path)
            self._model.set_data(dict)
            self._main_presenter.notify(Command.FILEREADSUCCESS)

        except ValueError as e:
            self._view.show_reject_file_message(str(e))


