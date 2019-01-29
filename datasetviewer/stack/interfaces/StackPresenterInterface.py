from abc import ABC, abstractmethod

class StackPresenterInterface(ABC):

    @abstractmethod
    def register_master(self, master):
        pass

    @abstractmethod
    def set_dict(self, dict):
        pass

    @abstractmethod
    def create_default_button_press(self, key):
        pass

    @abstractmethod
    def change_stack_face(self, key):
        pass

    @abstractmethod
    def x_button_change(self, dim_name, state):
        pass

    @abstractmethod
    def y_button_change(self, dim_name, state):
        pass

    @abstractmethod
    def slice_change(self):
        pass

    @abstractmethod
    def _dims_with_x_checked(self):
        pass

    @abstractmethod
    def _dims_with_y_checked(self):
        pass

    @abstractmethod
    def _create_slice_dictionary(self):
        pass

    @abstractmethod
    def _clear_stack(self):
        pass
