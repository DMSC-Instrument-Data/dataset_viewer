from datasetviewer.fileloader.FileLoaderTool import FileLoaderTool
from datasetviewer.mainview.interfaces.MainViewPresenterInterface import MainViewPresenterInterface


class MainViewPresenter(MainViewPresenterInterface):

    def __init__(self, mainview, *subpresenters):

        if mainview is None:
            raise ValueError("Error: Cannot create MainViewPresenter when MainView is None.")

        self._main_view = mainview
        self._subpresenters = []
        self._preview_presenter = None
        self._file_reader = FileLoaderTool()

        for presenter in subpresenters:

            if presenter is None:
                raise ValueError("Error: Cannot create MainViewPresenter when a SubPresenter is None.")

            presenter.register_master(self)

    def set_data(self, dict):

        self._data = dict
        self._preview_presenter.set_data(dict)

    def subscribe_preview_presenter(self, prev):

        self._preview_presenter = prev

    def subscribe_subpresenter(self, *subpresenter):

        self._subpresenters.append(subpresenter)
