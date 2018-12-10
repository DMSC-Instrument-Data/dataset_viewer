from datasetviewer.commands import Command

class PreviewPresenter(object):

    def __init__(self, view, source):

        if view is None:
            raise ValueError("Error: Cannot create Presenter when View is None.")

        if source is None:
            raise ValueError("Error: Cannot create Presenter when Source is None.")

        self._view = view
        self._source = source

    def create_preview_text(self, name):

        data = self._source.get_element(name)
        dims = data.dimension_size

        return name + "\n" + str(dims)

    def add_preview_entry(self, name):
        pass

    def notify(self, command):
        pass
