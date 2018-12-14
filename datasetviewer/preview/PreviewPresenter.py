from datasetviewer.preview.Command import Command as PreviewCommand
from datasetviewer.fileloader.Command import Command as FileCommand
from datasetviewer.presenter.SubPresenter import SubPresenter
from datasetviewer.mainview.interfaces.MainViewPresenterInterface import MainViewPresenterInterface


class PreviewPresenter(SubPresenter):

    def __init__(self, view, source):

        if view is None:
            raise ValueError("Error: Cannot create PreviewPresenter when View is None.")

        if source is None:
            raise ValueError("Error: Cannot create PreviewPresenter when Source is None.")

        self._view = view
        self._source = source

    def register_master(self, master):

        assert (isinstance(master, MainViewPresenterInterface))

        self._main_presenter = master
        self._main_presenter.subscribe_subpresenter(self)

    def create_preview_text(self, name):

        data = self._source.get_element(name)
        dims = data.dimension_size

        return name + "\n" + str(dims)

    def add_preview_entry(self, name):

        entry_text = self.create_preview_text(name)
        self._view.add_entry_to_list(entry_text)

    def populate_preview_list(self):

        data = self._source.get_data()

        for key, _ in data.items():
            self.add_preview_entry(key)

    def notify(self, command):

        if command == PreviewCommand.ARRAYSELECTION:
            # Load the selected array into the plot
            pass

        elif command == FileCommand.FILEREADSUCCESS:
            self.populate_preview_list()

        else:
            raise ValueError("PreviewPresenter received an unrecognised command: {}".format(str(command)))
