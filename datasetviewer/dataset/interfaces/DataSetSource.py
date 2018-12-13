from abc import ABC, abstractmethod


class DataSetSource(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def get_element(self, name):
        pass

    @abstractmethod
    def get_array(self):
        pass

    @abstractmethod
    def get_keys(self):
        pass

    @abstractmethod
    def set_data(self, data):
        pass