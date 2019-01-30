from datasetviewer.dimension.interfaces.DimensionPresenterInterface import DimensionPresenterInterface
from datasetviewer.stack.interfaces.StackPresenterInterface import StackPresenterInterface
from datasetviewer.dimension.Command import Command

class DimensionPresenter(DimensionPresenterInterface):
    """

    Presenter for overseeing the behaviour of the X/Y buttons, slider, and stepper for a single dimension. Prevents
    unchecking of an X button or having two buttons checked on the same dimension. Also makes sure that slider and
    stepper are in sync. Answers to StackPresenter rather than MainViewPresenter when user interacts with the
    DimensionView elements.

    Private Attributes:
        _view (DimensionView): The DimensionView object. Set in constructor.
        _dim_name (str): The name of this dimension. Required when communicating with StackPresenter so that it knows
            which dimension called it.
        _stack_master (StackPresenter): The StackPresenter that controls all DimensionPresenters. Defaults to None.
        _enabled (bool): Used to determine if a Dimension is enabled or not. When a button is successfully pressed on
            a button then it becomes disabled and its slider and stepper become hidden.

    Raises:
        ValueError: If the `dim_view` or `dim_name` are None.

    """

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
        """

        Interpret a command from the DimensionView and take the appropriate action.

        Note:
            `register_stack_master` must be called before this method can be called.

        Args:
            command (Command): A Command from the DimensionView indicating that an event has taken place.

        Raises:
            ValueError: If the command isn't recognised.

        """

        if command == Command.XBUTTONCHANGE:

            new_x_state = self._view.get_x_state()

            '''
            Undo the change in X if this results in the X button being unchecked, or if the press took place on a
            Dimension for which the Y button has already been checked.
            '''
            if (new_x_state and self._view.get_y_state()) \
                    or not new_x_state:
                self._view.set_x_state(not new_x_state)

            else:
                self._stack_master.x_button_change(self._dim_name, new_x_state)

        elif command == Command.YBUTTONCHANGE:

            new_y_state = self._view.get_y_state()

            '''
            Undo the change on Y if the press took place on a Dimension for which the X button has already been checked.
            '''
            if new_y_state and self._view.get_x_state():
                self._view.set_y_state(not new_y_state)

            else:
                self._stack_master.y_button_change(self._dim_name, new_y_state)

        elif command == Command.SLIDERCHANGE:

            # Update the stepper value and then inform the StackPresenter
            new_slider_val = self._view.get_slider_value()
            self._view.set_stepper_value(new_slider_val)
            self._stack_master.slice_change()

        elif command == Command.STEPPERCHANGE:

            # Update the slider value and then inform the StackPresenter
            new_stepper_val = self._view.get_stepper_value()
            self._view.set_slider_value(new_stepper_val)
            self._stack_master.slice_change()

        else:
            raise ValueError("DimensionPresenter received an unrecognised command: {}".format(str(command)))

    def register_stack_master(self, stack_master):
        """

        Register the StackPresenter as the DimensionPresenter's master.

        Args:
            stack_master (StackPresenter): An instance of a StackPresenter.

        """
        assert (isinstance(stack_master, StackPresenterInterface))

        self._stack_master = stack_master

    def get_x_state(self):
        """ Determine if the X button associated with this Presenter is checked or unchecked.

        Returns:
            bool: True if the button is checked and False if the button is unchecked.

        """

        return self._view.get_x_state()

    def set_x_state(self, state):
        """

        Set the state of the X button controlled by this Presenter.

        Args:
            state (bool): The new state for the X button.

        """

        self._view.set_x_state(state)

    def get_y_state(self):
        """ Determine if the Y button associated with this Presenter is checked or unchecked.

        Returns:
            bool: True if the button is checked and False if the button is unchecked.

        """

        return self._view.get_y_state()

    def set_y_state(self, state):
        """

        Set the state of the Y button controlled by this Presenter.

        Args:
            state (bool): The new state for the Y button.

        """

        self._view.set_y_state(state)

    def enable_dimension(self):
        """
        Enable a dimension by making its slider and stepper usable, and by unchecking its X and Y buttons.
        """

        self._view.enable_slider()
        self._view.enable_stepper()
        self._view.set_x_state(False)
        self._view.set_y_state(False)
        self._enabled = True

    def disable_dimension(self):
        """
        Disable a dimension by hiding its slider and stepper. Checking the X/Y button is handled when the user makes
        this action.
        """

        self._view.disable_slider()
        self._view.disable_stepper()
        self._enabled = False

    def is_enabled(self):
        """
        Determine if a dimension is "enabled" (it is not an X or Y axis so its sliders may be used) or "disabled" (it
        is being used as an X or Y axis so its slider and stepper are invisible). Used for determining how to slice
        the data array.

        Returns:
            bool: True if the Dimension is enabled and False if the Dimension is disabled.

        """

        return self._enabled

    def get_slider_value(self):
        """
        Obtain the current slider value on the DimensionView. This should be in sync with the stepper, so there is no
        equivalent method for finding the stepper value.

        Returns:
            int: The current value of the slider (and stepper).
        """

        return self._view.get_slider_value()

    def reset_slice(self):

        self._block_signal(True)
        self._view.set_slider_value(0)
        self._view.set_stepper_value(0)
        self._block_signal(False)

    def _block_signal(self, bool):

        self._view.block_signal(bool)
