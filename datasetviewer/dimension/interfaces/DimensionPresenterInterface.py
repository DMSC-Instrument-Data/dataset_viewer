from abc import ABC, abstractmethod

class DimensionPresenterInterface(ABC):

    @abstractmethod
    def register_stack_master(self, stack_master):
        pass

    @abstractmethod
    def notify(self, command):
        pass

    @abstractmethod
    def set_x_state(self, state):
        pass

    @abstractmethod
    def set_y_state(self, state):
        pass
