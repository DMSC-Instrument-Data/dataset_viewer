from datasetviewer.preview.Command import Command as PreviewCommand
from datasetviewer.fileloader.Command import Command as FileCommand


class MainViewPresenter(object):

    def __init__(self, mainview, *subpresenters):

        self._main_view = mainview

        for presenter in subpresenters:
            presenter.register_master(self)

    def subscribe_subpresenter(self, *subpresenter):
        pass

    def notify(self, command):

        if command == PreviewCommand.ARRAYSELECTION:
            # Retrieve key of current selection from preview view
            # Get data corresponding with key from data source model
            # Send data to plot view
            pass
        elif command == FileCommand.FILESELECTION:
            # Get file location from view
            # Load/validate file?
            # Convert to xarray format
            # Validate array?
            # Send array to model
            # Tell preview presenter to update preview view
            pass
        else:
            raise ValueError("PreviewPresenter received an unrecognised command: {}".format(str(command)))
