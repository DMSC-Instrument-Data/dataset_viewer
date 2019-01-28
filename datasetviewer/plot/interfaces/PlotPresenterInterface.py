from abc import ABC, abstractmethod

class PlotPresenterInterface(ABC):

    @abstractmethod
    def create_default_plot(self, data):
        pass

    @abstractmethod
    def _clear_plot(self):
        pass

    @abstractmethod
    def register_master(self, master):
        pass

    @abstractmethod
    def _draw_plot(self):
        pass

    @abstractmethod
    def set_dict(self, dict):
        pass

    @abstractmethod
    def create_onedim_plot(self, key, x_dim, slice):
        pass
