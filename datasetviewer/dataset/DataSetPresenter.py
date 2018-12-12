from datasetviewer.dataset.FileReader import FileReader


class DataSetPresenter(object):

    def __init__(self, data_set_source, preview_view):

        self._model = data_set_source
        self._main_presenter = None
        self._view = preview_view

    def register_master(self, master):

        self._main_presenter = master
        master.subscribe_subpresenter(self)

    def load_dictionary_to_model(self, file_path):
        pass
