from datasetviewer.fileloader.FileLoaderTool import FileLoaderTool
from datasetviewer.preview.Command import Command as PreviewCommand
from datasetviewer.mainview.interfaces.MainViewPresenterInterface import MainViewPresenterInterface


class MainViewPresenter(MainViewPresenterInterface):

    def __init__(self, mainview, data_set_source, *subpresenters):

        if mainview is None:
            raise ValueError("Error: Cannot create MainViewPresenter when MainView is None.")

        self._main_view = mainview
        self._model = data_set_source
        self._subpresenters = []
        self._preview_presenter = None
        self._file_reader = FileLoaderTool()

        for presenter in subpresenters:

            if presenter is None:
                raise ValueError("Error: Cannot create MainViewPresenter when a SubPresenter is None.")

            presenter.register_master(self)

    def load_file_to_model(self, file_path):
        pass

    def subscribe_preview_presenter(self, prev):

        self._preview_presenter = prev

    def subscribe_subpresenter(self, *subpresenter):

        self._subpresenters.append(subpresenter)

    def create_preview(self):

        self._preview_presenter.populate_preview_list()

