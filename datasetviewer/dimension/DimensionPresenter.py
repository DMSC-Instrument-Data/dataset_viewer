from datasetviewer.dimension.interfaces.DimensionPresenterInterface import DimensionPresenterInterface
from datasetviewer.stack.interfaces.StackPresenterInterface import StackPresenterInterface
from datasetviewer.dimension.Command import Command

class DimensionPresenter(DimensionPresenterInterface):

    def __init__(self, dim_view, dim_name):

        if dim_view is None:
            raise ValueError("Error: Cannot create DimensionPresenter when View is None.")

        if dim_name is None:
            raise ValueError("Error: Cannot create DimensionPresenter when Name is None.")

        self._view = dim_view
        self._dim_name = dim_name
        self._stack_master = None
        self._enabled = True

    def notify(self, command):

        if command == Command.XBUTTONPRESS:

            new_x_state = self._view.get_x_state()

            if (new_x_state and self._view.get_y_state()) \
                    or not new_x_state:
                self._view.set_x_state(not new_x_state)

            else:
                self._stack_master.x_button_change(self._dim_name, new_x_state)

        elif command == Command.YBUTTONPRESS:

            new_y_state = self._view.get_y_state()

            if new_y_state and self._view.get_x_state():
                self._view.set_y_state(not new_y_state)

            else:
                self._stack_master.y_button_change(self._dim_name, new_y_state)

        elif command == Command.SLIDERCHANGE:

            new_slider_val = self._view.get_slider_value()
            self._view.set_stepper_value(new_slider_val)
            self._stack_master.slice_change()

        elif command == Command.STEPPERCHANGE:

            new_stepper_val = self._view.get_stepper_value()
            self._view.set_slider_value(new_stepper_val)
            self._stack_master.slice_change()

        else:
            raise ValueError("DimensionPresenter received an unrecognised command: {}".format(str(command)))

    def register_stack_master(self, stack_master):

        assert (isinstance(stack_master, StackPresenterInterface))

        self._stack_master = stack_master

    def set_x_state(self, state):

        self._view.set_x_state(state)

    def set_y_state(self, state):

        self._view.set_y_state(state)

    def enable_dimension(self):

        self._view.enable_slider()
        self._view.enable_stepper()
        self._view.set_x_state(False)
        self._view.set_y_state(False)
        self._enabled = True

    def disable_dimension(self):

        self._view.disable_slider()
        self._view.disable_stepper()
        self._enabled = False

    def is_enabled(self):
        return self._enabled

    def get_slider_value(self):
        return self._view.get_slider_value()
