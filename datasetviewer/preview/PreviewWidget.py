from datasetviewer.preview.interfaces.PreviewViewInterface import PreviewViewInterface
from datasetviewer.preview.PreviewPresenter import PreviewPresenter

from PyQt5.QtWidgets import QListWidget

from abc import ABCMeta
from sip import wrappertype

class Template(ABCMeta, wrappertype):
    pass

class PreviewWidget(QListWidget, PreviewViewInterface, metaclass=Template):

    def __init__(self, parent = None):

        QListWidget.__init__(self, parent)

        self._presenter = PreviewPresenter(self)

    def add_entry_to_list(self, entry_text):
        self.addItem(entry_text)

    def get_presenter(self):
        return self._presenter