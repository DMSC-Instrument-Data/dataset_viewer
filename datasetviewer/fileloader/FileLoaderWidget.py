from datasetviewer.fileloader.interfaces.FileLoaderViewInterface import FileLoaderViewInterface
from datasetviewer.fileloader.FileLoaderPresenter import FileLoaderPresenter
from datasetviewer.fileloader.Command import Command

from PyQt5.QtWidgets import QFileDialog, QAction, QErrorMessage

class FileLoaderWidget(QAction, FileLoaderViewInterface):

    def __init__(self, parent = None):

        QAction.__init__(self, parent, text="Open...")

        self.parent = parent

        # Placeholder for the filename
        self.fname = None

        # Action for opening a file
        self.triggered.connect(self.open_file)

        # Create a FileLoaderPresenter and give it a reference to the FileLoaderView
        self._presenter = FileLoaderPresenter(self)

    def get_selected_file_path(self):
        return self.fname

    def show_reject_file_message(self, error_msg):
        '''
        Error message displayed when the chosen file couldn't be read into an xarray. Simply a copy of the exception
        thrown during file reading.
        '''

        error_dialog = QErrorMessage()
        error_dialog.showMessage(error_msg)
        error_dialog.exec_()

    def open_file(self):

        # Create and show a file dialog with a NetCDF filter
        filedialog = QFileDialog()

        # Store the location of the file that was selected
        self.fname = filedialog.getOpenFileName(self.parent, "Open file", "/home", "NetCDF (*.nc)")

        # Inform the presenter that the user attempted to open a file
        self._presenter.notify(Command.FILEOPENREQUEST)

    def get_presenter(self):
        return self._presenter
