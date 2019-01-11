from datasetviewer.preview.interfaces.PreviewViewInterface import PreviewViewInterface
from datasetviewer.preview.PreviewPresenter import PreviewPresenter

from PyQt5.QtWidgets import QListWidget

class PreviewWidget(PreviewViewInterface, QListWidget):

    def __init__(self, parent = None):

        QListWidget.__init__(self, parent)

        self.selected_item = None

        self._presenter = PreviewPresenter(self)
        self.itemDoubleClicked.connect(self.record_selection)

    def add_entry_to_list(self, entry_text):
        self.addItem(entry_text)

    def record_selection(self, item):
        pass
        # print()

    def get_selected_item(self):
        pass

    def get_presenter(self):
        return self._presenter
