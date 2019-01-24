from abc import ABC, abstractmethod

class StackPresenterInterface(ABC):

    @abstractmethod
    def register_master(self, master):
        pass

    @abstractmethod
    def set_dict(self, dict):
        pass

    @abstractmethod
    def create_default_button_press(self):
        pass

    @abstractmethod
    def change_stack_face(self, key):
        pass

    @abstractmethod
    def x_button_press(self, dim_name, state):
        pass

    @abstractmethod
    def y_button_press(self, dim_name, state):
        pass

    @abstractmethod
    def slider_change(self, dim_name, val):
        pass
