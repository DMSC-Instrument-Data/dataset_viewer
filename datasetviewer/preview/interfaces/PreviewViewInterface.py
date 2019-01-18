from abc import ABCMeta, abstractmethod
from PyQt5 import QtCore

from six import with_metaclass

class Meta(ABCMeta, type(QtCore.QObject)):
    pass

class PreviewViewInterface(with_metaclass(Meta)):

    @abstractmethod
    def add_entry_to_list(self, entry_text):
        pass

    @abstractmethod
    def clear_selection(self):
        pass

    @abstractmethod
    def get_presenter(self):
        pass

    @abstractmethod
    def record_selection(self, item):
        pass

    @abstractmethod
    def get_selected_item(self):
        pass

    @abstractmethod
    def clear_preview(self):
        pass
