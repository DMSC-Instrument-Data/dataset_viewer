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

    @abstractmethod
    def stepper_change(self, dim_name, val):
        pass

    @abstractmethod
    def _dims_with_x_pressed(self):
        pass

    @abstractmethod
    def _dims_with_y_pressed(self):
        pass

    @abstractmethod
    def _same_dim_has_x_and_y_pressed(self, dims_with_x_pressed, dims_with_y_pressed):
        pass
