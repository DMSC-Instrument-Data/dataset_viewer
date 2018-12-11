from datasetviewer.preview.Command import Command as PreviewCommand
from datasetviewer.datasource.Command import Command as DataCommand

class MainViewPresenter(object):

    def __init__(self, mainview, *subpresenters):

        self._main_view = mainview

        for presenter in subpresenters:
            presenter.register_master(self)

    def notify(self, command):

        if command == PreviewCommand.ARRAYSELECTION:
            pass
        elif command == DataCommand.FILESELECTION:
            pass
        else:
            raise ValueError("PreviewPresenter received an unrecognised command: {}".format(str(command)))
