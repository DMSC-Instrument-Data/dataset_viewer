from abc import ABCMeta, abstractmethod
from PyQt5 import QtCore

from six import with_metaclass

class Meta(ABCMeta, type(QtCore.QObject)):
    pass

class PreviewViewInterface(with_metaclass(Meta)):

    @abstractmethod
    def add_entry_to_list(self, entry_text):
        pass
