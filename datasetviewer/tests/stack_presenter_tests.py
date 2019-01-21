import unittest
from unittest import mock

from datasetviewer.stack.StackPresenter import StackPresenter
from datasetviewer.stack.interfaces.StackViewInterface import StackViewInterface
from datasetviewer.dimension.interfaces.DimensionViewFactoryInterface import DimensionViewFactoryInterface
from datasetviewer.mainview.interfaces.MainViewPresenterInterface import MainViewPresenterInterface

class StackPresenterTest(unittest.TestCase):

    def setUp(self):

        self.mock_main_presenter = mock.create_autospec(MainViewPresenterInterface)
        self.mock_stack_view = mock.create_autospec(StackViewInterface)
        self.mock_dim_fact = mock.create_autospec(DimensionViewFactoryInterface)

    def test_presenter_throws_if_args_none(self):

        with self.assertRaises(ValueError):
            StackPresenter(None, self.mock_dim_fact)

        with self.assertRaises(ValueError):
            StackPresenter(self.mock_stack_view, None)

    def test_register_master(self):

        stack_pres = StackPresenter(self.mock_stack_view, self.mock_dim_fact)
        stack_pres.register_master(self.mock_main_presenter)

        self.mock_main_presenter.subscribe_stack_presenter.assert_called_once_with(stack_pres)

    def test_clear_stack(self):
        pass
