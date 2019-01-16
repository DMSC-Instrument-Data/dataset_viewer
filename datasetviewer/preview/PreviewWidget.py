from datasetviewer.preview.interfaces.PreviewViewInterface import PreviewViewInterface
from datasetviewer.preview.PreviewPresenter import PreviewPresenter
from datasetviewer.preview.Command import Command

from PyQt5.QtWidgets import QListWidget

class PreviewWidget(PreviewViewInterface, QListWidget):

    def __init__(self, parent = None):

        QListWidget.__init__(self, parent)

        self.selected_item = None

        self._presenter = PreviewPresenter(self)
        self.itemClicked.connect(self.record_selection)

    def add_entry_to_list(self, entry_text):
        self.addItem(entry_text)

    def record_selection(self, item):
        self.selected_item = item
        self._presenter.notify(Command.ELEMENTSELECTION)

    def get_selected_item(self):
        return self.selected_item

    def get_presenter(self):
        return self._presenter
