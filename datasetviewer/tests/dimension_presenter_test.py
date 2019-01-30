import unittest
from unittest import mock

from enum import Enum

from datasetviewer.stack.interfaces.StackPresenterInterface import StackPresenterInterface
from datasetviewer.dimension.interfaces.DimensionViewInterface import DimensionViewInterface
from datasetviewer.dimension.DimensionPresenter import DimensionPresenter
from datasetviewer.dimension.Command import Command

class DimensionPresenterTest(unittest.TestCase):

    def setUp(self):

        self.mock_dim_view = mock.create_autospec(DimensionViewInterface)
        self.mock_stack_pres = mock.create_autospec(StackPresenterInterface)

        self.fake_dim_name = 'y'

    def test_constructor_throws_if_args_none(self):
        ''' Test that the expected Exceptions are thrown when the DimensionPresenter received bad arguments. '''

        with self.assertRaises(ValueError):
            DimensionPresenter(self.mock_dim_view, None)

        with self.assertRaises(ValueError):
            DimensionPresenter(None, self.fake_dim_name)

    def test_notify_x_press_calls_stack(self):
        ''' Test that calling `notify` with the XBUTTONCHANGE command causes the button state to be retrieved from the
        DimensionView, and calls the `x_button_change` method in the StackPresenter. '''

        # Give the mock a fake X state, and set its Y button to the opposite of that state
        fake_x_state = True
        self.mock_dim_view.get_x_state = mock.MagicMock(return_value = fake_x_state)
        self.mock_dim_view.get_y_state = mock.MagicMock(return_value = not fake_x_state)

        dim_pres = DimensionPresenter(self.mock_dim_view, self.fake_dim_name)
        dim_pres.register_stack_master(self.mock_stack_pres)

        dim_pres.notify(Command.XBUTTONCHANGE)
        self.mock_dim_view.get_x_state.assert_called_once()
        self.mock_stack_pres.x_button_change.assert_called_once_with(self.fake_dim_name, fake_x_state)

    def test_notify_y_press_calls_stack(self):
        ''' Test that calling `notify` with the YBUTTONCHANGE command causes the button state to be retrieved from the
        DimensionView, and calls the `y_button_change` method in the StackPresenter. '''

        fake_y_state = False
        self.mock_dim_view.get_x_state = mock.MagicMock(return_value = not fake_y_state)
        self.mock_dim_view.get_y_state = mock.MagicMock(return_value = fake_y_state)

        dim_pres = DimensionPresenter(self.mock_dim_view, self.fake_dim_name)
        dim_pres.register_stack_master(self.mock_stack_pres)

        dim_pres.notify(Command.YBUTTONCHANGE)
        self.mock_dim_view.get_y_state.assert_called_once()
        self.mock_stack_pres.y_button_change.assert_called_once_with(self.fake_dim_name, fake_y_state)

    def test_notify_x_press_reverts_press(self):
        ''' Test that attempting to check an X button when the Y button for this dimension has already been pressed
        causes the action to be reversed. '''

        # Create a mock DimensionView with "checked" X and Y buttons
        fake_x_state = True
        self.mock_dim_view.get_x_state = mock.MagicMock(return_value = fake_x_state)
        self.mock_dim_view.get_y_state = mock.MagicMock(return_value = fake_x_state)

        dim_pres = DimensionPresenter(self.mock_dim_view, self.fake_dim_name)
        dim_pres.register_stack_master(self.mock_stack_pres)

        '''
        Inform the DimensionPresenter that the X button's state has changed. This means it will be viewed as the most
        recent press.
        '''
        dim_pres.notify(Command.XBUTTONCHANGE)

        '''
        Check that the X button state was switched back to False, and that this action did not trigger a response in
        the StackPresenter.
        '''
        self.mock_dim_view.set_x_state.assert_called_once_with(not fake_x_state)
        self.mock_stack_pres.x_button_change.assert_not_called()

    def test_notify_y_press_reverts_press(self):
        ''' Test that attempting to check an Y button when the X button for this dimension has already been pressed
        causes the action to be reversed. '''

        # Create a mock DimensionView with "checked" X and Y buttons
        fake_y_state = True
        self.mock_dim_view.get_x_state = mock.MagicMock(return_value = fake_y_state)
        self.mock_dim_view.get_y_state = mock.MagicMock(return_value = fake_y_state)

        dim_pres = DimensionPresenter(self.mock_dim_view, self.fake_dim_name)
        dim_pres.register_stack_master(self.mock_stack_pres)

        '''
        Inform the DimensionPresenter that the X button's state has changed. This means it will be viewed as the most
        recent press.
        '''
        dim_pres.notify(Command.YBUTTONCHANGE)

        '''
        Check that the Y button state was switched back to False, and that this action did not trigger a response in
        the StackPresenter.
        '''
        self.mock_dim_view.set_y_state.assert_called_once_with(not fake_y_state)
        self.mock_stack_pres.y_button_change.assert_not_called()

    def test_x_cannot_be_unchecked(self):
        ''' Test that an X which has been checked cannot be unchecked. Changing the x-axis can should be accomplished by
        selecting another dimension that is not being used for the y-axis. '''

        # Create a mock DimensionView with an unchecked X and Y
        fake_x_state = False
        self.mock_dim_view.get_x_state = mock.MagicMock(return_value = fake_x_state)
        self.mock_dim_view.get_y_state = mock.MagicMock(return_value = fake_x_state)

        dim_pres = DimensionPresenter(self.mock_dim_view, self.fake_dim_name)
        dim_pres.register_stack_master(self.mock_stack_pres)

        # Use notify to indicate that the X button state has changed (i.e. it is now False but was previously True)
        dim_pres.notify(Command.XBUTTONCHANGE)

        '''
        Check that the X button is set back to being checked, and that this action did not trigger a response in the
        StackPresenter.
        '''
        self.mock_dim_view.set_x_state.assert_called_once_with(not fake_x_state)
        self.mock_stack_pres.x_button_change.assert_not_called()

    def test_notify_slider_change(self):
        ''' Test that the SLIDERCHANGE command in the DimensionPresenter causes it to retrieve the slider value, set the
        stepper to this value, and then inform the StackPresenter of the change. '''

        # Create a fake slider value and have the mock DimensionView return this value
        fake_slider_value = 2
        self.mock_dim_view.get_slider_value = mock.MagicMock(return_value = fake_slider_value)

        dim_pres = DimensionPresenter(self.mock_dim_view, self.fake_dim_name)
        dim_pres.register_stack_master(self.mock_stack_pres)

        dim_pres.notify(Command.SLIDERCHANGE)

        self.mock_dim_view.get_slider_value.assert_called_once()
        self.mock_dim_view.set_stepper_value.assert_called_once_with(fake_slider_value)
        self.mock_stack_pres.slice_change.assert_called_once()

    def test_notify_stepper_change(self):
        ''' Test that the STEPPERCHANGE command in the DimensionPresenter causes it to retrieve the slider value, set
        the stepper to this value, and then inform the StackPresenter of the change. '''

        # Create a fake stepper value and have the mock DimensionView return this value

        fake_stepper_value = 3
        self.mock_dim_view.get_stepper_value = mock.MagicMock(return_value = fake_stepper_value)

        dim_pres = DimensionPresenter(self.mock_dim_view, self.fake_dim_name)
        dim_pres.register_stack_master(self.mock_stack_pres)

        dim_pres.notify(Command.STEPPERCHANGE)
        self.mock_dim_view.get_stepper_value.assert_called_once()
        self.mock_dim_view.set_slider_value.assert_called_once_with(fake_stepper_value)
        self.mock_stack_pres.slice_change.assert_called_once()

    def test_notify_throws(self):
        ''' Test that the `notify` method throws an Exception when it receives an unexpected command. '''

        # Create a fake command/enum
        fake_enum = Enum(value='invalid', names=[('bad_command', -200000)])

        dim_pres = DimensionPresenter(self.mock_dim_view, self.fake_dim_name)

        with self.assertRaises(ValueError):
            dim_pres.notify(fake_enum)

    def test_get_x_state(self):
        ''' Test that getting the X state from the DimensionPresenter causes a method with the same name to be called on
        the DimensionView. '''

        dim_pres = DimensionPresenter(self.mock_dim_view, self.fake_dim_name)
        dim_pres.get_x_state()
        self.mock_dim_view.get_x_state.assert_called_once()

    def test_set_x_state(self):
        ''' Test that setting the X state from the DimensionPresenter causes a method with the same name to be called on
        the DimensionView. '''

        dim_pres = DimensionPresenter(self.mock_dim_view, self.fake_dim_name)
        desired_x_state = True
        dim_pres.set_x_state(desired_x_state)
        self.mock_dim_view.set_x_state.assert_called_once_with(desired_x_state)

    def test_get_y_state(self):
        ''' Test that getting the Y state from the DimensionPresenter causes a method with the same name to be called on
        the DimensionView. '''

        dim_pres = DimensionPresenter(self.mock_dim_view, self.fake_dim_name)
        dim_pres.get_y_state()
        self.mock_dim_view.get_y_state.assert_called_once()

    def test_set_y_state(self):
        ''' Test that setting the X state from the DimensionPresenter causes a method with the same name to be called on
        the DimensionView. '''

        dim_pres = DimensionPresenter(self.mock_dim_view, self.fake_dim_name)
        desired_y_state = True
        dim_pres.set_y_state(desired_y_state)
        self.mock_dim_view.set_y_state.assert_called_once_with(desired_y_state)

    def test_enable_and_disable_dimension(self):
        ''' Test that the expected elements on the DimensionView are made visible/invisible when the enabled and
        disable methods are called. '''

        dim_pres = DimensionPresenter(self.mock_dim_view, self.fake_dim_name)

        # Check that the slider and stepper have become visible, and that the X and Y states are now False/unchecked
        dim_pres.enable_dimension()
        self.mock_dim_view.enable_slider.assert_called_once()
        self.mock_dim_view.enable_stepper.assert_called_once()
        self.mock_dim_view.set_x_state.assert_called_once_with(False)
        self.mock_dim_view.set_y_state.assert_called_once_with(False)
        self.assertTrue(dim_pres.is_enabled())

        # Reset mock so previous function calls are forgotten
        self.mock_dim_view.reset_mock()

        # Check that the slider and stepper have become visible, and that the buttons are not altered.
        dim_pres.disable_dimension()
        self.mock_dim_view.disable_slider.assert_called_once()
        self.mock_dim_view.disable_stepper.assert_called_once()
        self.mock_dim_view.set_x_state.assert_not_called()
        self.mock_dim_view.set_y_state.assert_not_called()
        self.assertFalse(dim_pres.is_enabled())

    def test_get_slider_value(self):
        ''' Test that getting the slider value from the DimensionPresenter causes a method with the same name to be called in
        the DimensionView.'''

        dim_pres = DimensionPresenter(self.mock_dim_view, self.fake_dim_name)

        dim_pres.get_slider_value()
        self.mock_dim_view.get_slider_value.assert_called_once()

    def test_reset_slide(self):

        dim_pres = DimensionPresenter(self.mock_dim_view, self.fake_dim_name)

        dim_pres.reset_slice()

        self.mock_dim_view.set_slider_value.assert_called_once_with(0)
        self.mock_dim_view.set_stepper_value.assert_called_once_with(0)