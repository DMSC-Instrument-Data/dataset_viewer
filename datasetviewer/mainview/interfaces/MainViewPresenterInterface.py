from abc import ABC, abstractmethod

class MainViewPresenterInterface(ABC):

    @abstractmethod
    def subscribe_preview_presenter(self, prev):
        pass

    @abstractmethod
    def subscribe_plot_presenter(self, plot):
        pass

    @abstractmethod
    def subscribe_file_loader_presenter(self, file_loader):
        pass

    @abstractmethod
    def set_dict(self, dict):
        pass

    @abstractmethod
    def create_default_plot(self, key):
        pass

    @abstractmethod
    def update_toolbar(self):
        pass
