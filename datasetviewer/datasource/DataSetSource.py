from abc import ABC, abstractmethod


class DataSetSource(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def get_element(self, name):
        pass

    @abstractmethod
    def get_data(self):
        pass
