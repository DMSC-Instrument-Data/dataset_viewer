from datasetviewer.fileloader.FileReader import FileReader
from datasetviewer.presenter.SubPresenter import SubPresenter


class FileLoaderPresenter(SubPresenter):

    def __init__(self, data_set_source, preview_view):

        self._model = data_set_source
        self._main_presenter = None
        self._view = preview_view
        self._file_reader = FileReader()

    def register_master(self, master):

        self._main_presenter = master
        master.subscribe_subpresenter(self)

    def load_data_to_model(self, file_path):

        try:
            dict = self._file_reader.file_to_dict(file_path)
            self._model.set_data(dict)

        except ValueError as e:
            self._view.show_reject_file_message(str(e))
