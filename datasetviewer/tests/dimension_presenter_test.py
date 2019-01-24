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

        with self.assertRaises(ValueError):
            DimensionPresenter(self.mock_dim_view, None)

        with self.assertRaises(ValueError):
            DimensionPresenter(None, self.fake_dim_name)

    def test_notify_x_press(self):

        fake_x_state = False
        self.mock_dim_view.get_x_state = mock.MagicMock(return_value=fake_x_state)

        dim_pres = DimensionPresenter(self.mock_dim_view, self.fake_dim_name)
        dim_pres.register_stack_master(self.mock_stack_pres)

        dim_pres.notify(Command.XBUTTONPRESS)
        self.mock_dim_view.get_x_state.assert_called_once()
        self.mock_stack_pres.x_button_press.assert_called_once_with(self.fake_dim_name, fake_x_state)

    def test_notify_y_press(self):

        fake_y_state = False
        self.mock_dim_view.get_y_state = mock.MagicMock(return_value=fake_y_state)

        dim_pres = DimensionPresenter(self.mock_dim_view, self.fake_dim_name)
        dim_pres.register_stack_master(self.mock_stack_pres)

        dim_pres.notify(Command.YBUTTONPRESS)
        self.mock_dim_view.get_y_state.assert_called_once()
        self.mock_stack_pres.y_button_press.assert_called_once_with(self.fake_dim_name, fake_y_state)

    def test_notify_slider_change(self):

        fake_slider_value = 2
        self.mock_dim_view.get_slider_value = mock.MagicMock(return_value = fake_slider_value)

        dim_pres = DimensionPresenter(self.mock_dim_view, self.fake_dim_name)
        dim_pres.register_stack_master(self.mock_stack_pres)

        dim_pres.notify(Command.SLIDERCHANGE)
        self.mock_dim_view.get_slider_value.assert_called_once()
        self.mock_dim_view.set_stepper_value.assert_called_once_with(fake_slider_value)
        self.mock_stack_pres.slider_change.assert_called_once_with(self.fake_dim_name, fake_slider_value)

    def test_notify_stepper_change(self):

        fake_stepper_value = 3
        self.mock_dim_view.get_stepper_value = mock.MagicMock(return_value = fake_stepper_value)

        dim_pres = DimensionPresenter(self.mock_dim_view, self.fake_dim_name)
        dim_pres.register_stack_master(self.mock_stack_pres)

        dim_pres.notify(Command.STEPPERCHANGE)
        self.mock_dim_view.get_stepper_value.assert_called_once()
        self.mock_dim_view.set_slider_value.assert_called_once_with(fake_stepper_value)
        self.mock_stack_pres.stepper_change.assert_called_once_with(self.fake_dim_name, fake_stepper_value)

    def test_notify_throws(self):

        # Create a fake command/enum
        fake_enum = Enum(value='invalid', names=[('bad_command', -200000)])

        dim_pres = DimensionPresenter(self.mock_dim_view, self.fake_dim_name)

        with self.assertRaises(ValueError):
            dim_pres.notify(fake_enum)

    def test_set_x_state(self):

        dim_pres = DimensionPresenter(self.mock_dim_view, self.fake_dim_name)
        dim_pres.set_x_state(True)
        self.mock_dim_view.set_x_state.assert_called_once_with(True)

    def test_set_y_state(self):

        dim_pres = DimensionPresenter(self.mock_dim_view, self.fake_dim_name)
        dim_pres.set_y_state(True)
        self.mock_dim_view.set_y_state.assert_called_once_with(True)
