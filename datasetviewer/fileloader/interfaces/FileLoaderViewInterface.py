from abc import ABCMeta, abstractmethod
from PyQt5 import QtCore

from six import with_metaclass

class Meta(ABCMeta, type(QtCore.QObject)):
    pass

class FileLoaderViewInterface(with_metaclass(Meta)):

    @abstractmethod
    def get_selected_file_path(self):
        pass

    @abstractmethod
    def show_reject_file_message(self, error_msg):
        pass

    @abstractmethod
    def open_file(self):
        pass

    @abstractmethod
    def get_presenter(self):
        pass
