from abc import ABC, abstractmethod

class SubPresenter(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def register_master(self, main_presenter):
        pass
