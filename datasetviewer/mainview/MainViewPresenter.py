from datasetviewer.preview.Command import Command as PreviewCommand
from datasetviewer.fileloader.Command import Command as FileCommand
from datasetviewer.mainview.interfaces.MainViewPresenterInterface import MainViewPresenterInterface


class MainViewPresenter(MainViewPresenterInterface):

    def __init__(self, mainview, *subpresenters):

        if mainview is None:
            raise ValueError("Error: Cannot create MainViewPresenter when MainView is None.")

        self._main_view = mainview
        self._subpresenters = []

        for presenter in subpresenters:

            if presenter is None:
                raise ValueError("Error: Cannot create MainViewPresenter when a SubPresenter is None.")

            presenter.register_master(self)

    def subscribe_subpresenter(self, *subpresenter):
        self._subpresenters.append(subpresenter)

    def notify(self, command):

        if command == PreviewCommand.ARRAYSELECTION:
            pass

        elif command == FileCommand.FILEREADSUCCESS:
            #
            pass
        else:
            raise ValueError("PreviewPresenter received an unrecognised command: {}".format(str(command)))
