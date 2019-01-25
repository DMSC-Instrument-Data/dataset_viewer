from abc import ABC, abstractmethod

class MainViewPresenterInterface(ABC):

    @abstractmethod
    def subscribe_preview_presenter(self, prev):
        pass

    @abstractmethod
    def subscribe_plot_presenter(self, plot):
        pass

    @abstractmethod
    def subscribe_stack_presenter(self, stack):
        pass

    @abstractmethod
    def set_dict(self, dict):
        pass

    @abstractmethod
    def change_current_key(self, key):
        pass

    @abstractmethod
    def update_toolbar(self):
        pass

    @abstractmethod
    def create_onedim_plot(self, key, x_dim, slice):
        pass
