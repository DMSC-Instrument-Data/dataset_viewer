from abc import ABC, abstractmethod

class MainViewPresenterInterface(ABC):

    @abstractmethod
    def subscribe_preview_presenter(self, prev):
        pass

    @abstractmethod
    def subscribe_plot_presenter(self, plot):
        pass

    @abstractmethod
    def subscribe_subpresenter(self, *subpresenter):
        pass

    @abstractmethod
    def set_data(self, data):
        pass

    @abstractmethod
    def create_default_plot(self, key):
        pass
