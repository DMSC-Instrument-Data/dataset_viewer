from abc import ABC, abstractmethod

class SubPresenterInterface(ABC):

    @abstractmethod
    def register_master(self, main_presenter):
        pass
