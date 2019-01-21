import unittest
from unittest import mock

from datasetviewer.stack.StackPresenter import StackPresenter
from datasetviewer.stack.interfaces.StackViewInterface import StackViewInterface
from datasetviewer.dimension.interfaces.DimensionViewFactoryInterface import DimensionViewFactoryInterface

class StackPresenterTest(unittest.TestCase):

    def setUp(self):

        self.mock_stack_view = mock.create_autospec(StackViewInterface)
        self.mock_dim_fact = mock.create_autospec(DimensionViewFactoryInterface)

    def test_presenter_throws_if_args_none(self):

        with self.assertRaises(ValueError):
            StackPresenter(None, self.mock_dim_fact)

        with self.assertRaises(ValueError):
            StackPresenter(self.mock_stack_view, None)

    def test_register_master(self):
        pass

    def test_clear_stack(self):
        pass
