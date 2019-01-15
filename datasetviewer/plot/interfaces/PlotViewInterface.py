from abc import ABCMeta, abstractmethod
from PyQt5 import QtCore

from six import with_metaclass

class Meta(ABCMeta, type(QtCore.QObject)):
    pass

class PlotViewInterface(with_metaclass(Meta)):

    @abstractmethod
    def plot_image(self, arr):
        pass

    @abstractmethod
    def plot_line(self, arr):
        pass
