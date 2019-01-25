from abc import ABCMeta, abstractmethod
from PyQt5 import QtCore

from six import with_metaclass

class Meta(ABCMeta, type(QtCore.QObject)):
    pass

class StackViewInterface(with_metaclass(Meta)):

    @abstractmethod
    def clear_stack(self):
        pass

    @abstractmethod
    def create_stack_element(self, key):
        pass

    @abstractmethod
    def add_dimension_view(self, key, dim_view):
        pass

    @abstractmethod
    def change_stack_face(self, key):
        pass
