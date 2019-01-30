from abc import ABC, abstractmethod

class DimensionViewInterface(ABC):

    @abstractmethod
    def get_x_state(self):
        pass

    @abstractmethod
    def set_x_state(self, state):
        pass

    @abstractmethod
    def get_y_state(self):
        pass

    @abstractmethod
    def set_y_state(self, state):
        pass

    @abstractmethod
    def get_slider_value(self):
        pass

    @abstractmethod
    def set_slider_value(self, val):
        pass

    @abstractmethod
    def get_stepper_value(self):
        pass

    @abstractmethod
    def set_stepper_value(self, val):
        pass

    @abstractmethod
    def get_presenter(self):
        pass

    @abstractmethod
    def enable_slider(self):
        pass

    @abstractmethod
    def enable_stepper(self):
        pass

    @abstractmethod
    def disable_slider(self):
        pass

    @abstractmethod
    def disable_stepper(self):
        pass

    @abstractmethod
    def get_widgets(self):
        pass

    @abstractmethod
    def block_signal(self, bool):
        pass
