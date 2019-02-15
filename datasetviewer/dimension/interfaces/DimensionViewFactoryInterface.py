from abc import ABC, abstractmethod

class DimensionViewFactoryInterface(ABC):

    @abstractmethod
    def create_widgets(self, dim_name, dim_size):
        pass
