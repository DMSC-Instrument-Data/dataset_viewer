import unittest
from unittest import mock

from datasetviewer.stack.interfaces.StackPresenterInterface import StackPresenterInterface
from datasetviewer.dimension.interfaces.DimensionViewInterface import DimensionViewInterface
from datasetviewer.dimension.DimensionPresenter import DimensionPresenter
from datasetviewer.dimension.Command import Command

class DimensionPresenterTest(unittest.TestCase):

    def setUp(self):

        self.mock_dim_view = mock.create_autospec(DimensionViewInterface)
        self.mock_stack_pres = mock.create_autospec(StackPresenterInterface)

        self.fake_dim_name = 'y'

    def test_notify_x_press(self):

        fake_x_state = False
        self.mock_dim_view.get_x_state = mock.MagicMock(return_value=fake_x_state)

        dim_pres = DimensionPresenter(self.mock_dim_view, self.fake_dim_name)
        dim_pres.register_stack_master(self.mock_stack_pres)

        dim_pres.notify(Command.XBUTTONPRESS)
        self.mock_dim_view.get_x_state.assert_called_once()
        self.mock_stack_pres.x_button_press.assert_called_once_with(self.fake_dim_name, fake_x_state)
