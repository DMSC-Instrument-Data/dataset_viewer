from abc import ABCMeta, abstractmethod
from PyQt5 import QtCore

from six import with_metaclass

class Meta(ABCMeta, type(QtCore.QObject)):
    pass

class MainViewInterface(with_metaclass(Meta)):

    @abstractmethod
    def update_toolbar(self):
        pass
