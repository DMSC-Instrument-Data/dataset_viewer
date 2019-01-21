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

    @abstractmethod
    def get_presenter(self):
        pass

    @abstractmethod
    def label_x_axis(self, label):
        pass

    @abstractmethod
    def label_y_axis(self, label):
        pass

    @abstractmethod
    def draw_plot(self):
        pass
