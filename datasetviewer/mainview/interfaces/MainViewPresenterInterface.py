from abc import ABC, abstractmethod

class MainViewPresenterInterface(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def subscribe_subpresenter(self, *subpresenter):
        pass

    @abstractmethod
    def notify(self, command):
        pass
