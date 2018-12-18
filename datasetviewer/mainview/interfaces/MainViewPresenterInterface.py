from abc import ABC, abstractmethod

class MainViewPresenterInterface(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def subscribe_subpresenter(self, *subpresenter):
        pass

    @abstractmethod
    def set_data(self, data):
        pass
