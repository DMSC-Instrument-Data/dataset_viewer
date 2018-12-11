from datasetviewer.preview.Command import Command

class PreviewPresenter(object):

    def __init__(self, view, source):

        if view is None:
            raise ValueError("Error: Cannot create PreviewPresenter when View is None.")

        if source is None:
            raise ValueError("Error: Cannot create PreviewPresenter when Source is None.")

        self._view = view
        self._source = source

    def create_preview_text(self, name):

        data = self._source.get_element(name)
        dims = data.dimension_size

        return name + "\n" + str(dims)

    def add_preview_entry(self, name):

        entry_text = self.create_preview_text(name)
        self._view.add_entry_to_list(entry_text)

    def populate_preview_list(self):

        data = self._source.get_data()

        for key,_ in data.items():
            self.add_preview_entry(key)

    def notify(self, command):

        if command == Command.SELECTION:
            pass
        else:
            raise ValueError("PreviewPresenter received an unrecognised command: {}".format(str(command)))
