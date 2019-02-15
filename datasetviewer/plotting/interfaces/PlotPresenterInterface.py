from abc import ABC, abstractmethod

class PlotPresenterInterface(ABC):

    @abstractmethod
    def change_current_key(self, data):
        pass

    @abstractmethod
    def _clear_plot(self):
        pass

    @abstractmethod
    def register_master(self, master):
        pass

    @abstractmethod
    def _update_plot(self):
        pass

    @abstractmethod
    def set_dict(self, dict):
        pass

    @abstractmethod
    def create_onedim_plot(self, key, x_dim, slice):
        pass

    @abstractmethod
    def create_twodim_plot(self, key, x_dim, y_dim, slice):
        pass