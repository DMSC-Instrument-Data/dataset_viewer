from abc import ABC, abstractmethod

class DimensionPresenterInterface(ABC):

    @abstractmethod
    def register_stack_master(self, stack_master):
        pass
