from datasetviewer.preview.interfaces.PreviewViewInterface import PreviewViewInterface
from datasetviewer.preview.PreviewPresenter import PreviewPresenter
from datasetviewer.preview.Command import Command

from PyQt5.QtWidgets import QListWidget

class PreviewWidget(PreviewViewInterface, QListWidget):

    def __init__(self, parent = None):

        QListWidget.__init__(self, parent)

        # Placeholder for the item that is currently selected
        self._selected_item = None

        # Create a PreviewPresenter and give it a reference to the PreviewView
        self._presenter = PreviewPresenter(self)
        self.itemSelectionChanged.connect(self.record_selection)
        self.setMinimumWidth(200)

    def reset_selection(self):
        self._selected_item = None

    def add_entry_to_list(self, entry_text):
        self.addItem(entry_text)

    def record_selection(self):
        self._selected_item = self.currentItem()
        self._presenter.notify(Command.ELEMENTSELECTION)

    def get_selected_item(self):
        return self._selected_item

    def get_presenter(self):
        return self._presenter

    def clear_preview(self):
        self.clear()

    def select_first_item(self):
        self.setCurrentItem(self.item(0))

    def block_signal(self, bool):
        self.blockSignals(bool)
