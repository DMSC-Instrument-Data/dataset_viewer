from abc import ABCMeta, abstractmethod
from PyQt5 import QtCore

from six import with_metaclass

class Meta(ABCMeta, type(QtCore.QObject)):
    pass

class DimensionViewInterface(with_metaclass(Meta)):

    @abstractmethod
    def get_x_state(self):
        pass

    @abstractmethod
    def set_x_state(self, state):
        pass

    @abstractmethod
    def get_y_state(self):
        pass

    @abstractmethod
    def set_y_state(self, state):
        pass

    @abstractmethod
    def get_slider_value(self):
        pass

    @abstractmethod
    def set_slider_value(self, val):
        pass

    @abstractmethod
    def get_stepper_value(self):
        pass

    @abstractmethod
    def set_stepper_value(self, val):
        pass

    @abstractmethod
    def get_presenter(self):
        pass

    @abstractmethod
    def enable_slider(self):
        pass

    @abstractmethod
    def enable_stepper(self):
        pass

    @abstractmethod
    def disable_slider(self):
        pass

    @abstractmethod
    def disable_stepper(self):
        pass
