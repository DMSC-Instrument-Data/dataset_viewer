from datasetviewer.preview.Command import Command as PreviewCommand
from datasetviewer.datasource.Command import Command as DataCommand

class MainViewPresenter(object):

    def __init__(self, mainview, *subpresenters):

        self._main_view = mainview

        for presenter in subpresenters:
            presenter.register_master(self)

    def notify(self, command):

        if command == PreviewCommand.ARRAYSELECTION:
            # Tell PlotView to plot this element in the dictionary
            pass
        elif command == DataCommand.FILESELECTION:
            # Load the file into the preview
            pass
        else:
            raise ValueError("PreviewPresenter received an unrecognised command: {}".format(str(command)))
