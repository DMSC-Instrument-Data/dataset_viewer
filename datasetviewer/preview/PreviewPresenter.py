from datasetviewer.presenter.SubPresenter import SubPresenter
from datasetviewer.mainview.interfaces.MainViewPresenterInterface import MainViewPresenterInterface


class PreviewPresenter(SubPresenter):

    def __init__(self, preview_view):

        if preview_view is None:
            raise ValueError("Error: Cannot create PreviewPresenter when View is None.")

        # View that contains the elements of the Preview Pane
        self._view = preview_view

        self._data = None

    def set_data(self, data):

        self._data = data
        self._populate_preview_list()

    def register_master(self, master):

        assert (isinstance(master, MainViewPresenterInterface))

        self._main_presenter = master
        self._main_presenter.subscribe_preview_presenter(self)

    def _create_preview_text(self, name):

        var = self._data[name]
        dims = var.get_dimensions()

        return name + "\n" + str(dims)

    def _add_preview_entry(self, name):

        entry_text = self._create_preview_text(name)
        self._view.add_entry_to_list(entry_text)

    def _populate_preview_list(self):

        for key, _ in self._data.items():
            self._add_preview_entry(key)

    def notify(self, command):
        pass
