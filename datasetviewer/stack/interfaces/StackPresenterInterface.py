from abc import ABC, abstractmethod

class StackPresenterInterface(ABC):

    @abstractmethod
    def register_master(self, master):
        pass

    @abstractmethod
    def set_dict(self, dict):
        pass
