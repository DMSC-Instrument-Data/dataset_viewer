from abc import ABC, abstractmethod

class DimensionViewFactoryInterface(ABC):

    @abstractmethod
    def create_widget(self, dim_name, size):
        pass
