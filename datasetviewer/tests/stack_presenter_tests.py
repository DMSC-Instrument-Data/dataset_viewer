import unittest
from unittest import mock

from datasetviewer.stack.StackPresenter import StackPresenter
from datasetviewer.stack.interfaces.StackViewInterface import StackViewInterface
from datasetviewer.dimension.interfaces.DimensionViewFactoryInterface import DimensionViewFactoryInterface
from datasetviewer.dimension.interfaces.DimensionViewInterface import DimensionViewInterface
from datasetviewer.mainview.interfaces.MainViewPresenterInterface import MainViewPresenterInterface

from collections import OrderedDict as DataSet
from datasetviewer.dataset.Variable import Variable
import xarray as xr
import numpy as np

class StackPresenterTest(unittest.TestCase):

    def setUp(self):

        self.mock_main_presenter = mock.create_autospec(MainViewPresenterInterface)
        self.mock_stack_view = mock.create_autospec(StackViewInterface)
        self.mock_dim_fact = mock.create_autospec(DimensionViewFactoryInterface)

        # Create a fake data dictionary with valid elements
        self.fake_dict = DataSet()
        self.fake_dict["threedims"] = Variable("threedims", xr.DataArray(np.random.rand(3, 4, 5), dims=['x', 'y', 'z']))
        self.fake_dict["onedim"] = Variable("onedim", xr.DataArray(np.random.rand(3), dims=['b']))
        self.fake_dict["twodims"] = Variable("twodims", xr.DataArray(np.random.rand(3, 8), dims=['g', 'h']))
        self.fake_dict["fourdims"] = Variable("fourdims",
                                              xr.DataArray(np.random.rand(3, 4, 5, 6), dims=['c', 'd', 'e', 'f']))

        self.mock_dim_widget = mock.create_autospec(DimensionViewInterface)
        self.mock_dim_fact.create_widget = mock.MagicMock(side_effect=lambda name,size: self.mock_dim_widget)

    def test_presenter_throws_if_args_none(self):
        ''' Test that exceptions are thrown if the DimensionViewFactory or StackView are None. '''

        with self.assertRaises(ValueError):
            StackPresenter(None, self.mock_dim_fact)

        with self.assertRaises(ValueError):
            StackPresenter(self.mock_stack_view, None)

    def test_register_master(self):
        ''' '''

        stack_pres = StackPresenter(self.mock_stack_view, self.mock_dim_fact)
        stack_pres.register_master(self.mock_main_presenter)

        self.mock_main_presenter.subscribe_stack_presenter.assert_called_once_with(stack_pres)

    def test_clear_stack(self):

        stack_pres = StackPresenter(self.mock_stack_view, self.mock_dim_fact)
        stack_pres.set_dict(self.fake_dict)

        self.mock_stack_view.clear_stack.assert_called_once()

    def test_correct_stacks_created(self):

        stack_pres = StackPresenter(self.mock_stack_view, self.mock_dim_fact)
        stack_pres.set_dict(self.fake_dict)

        self.assertEqual(self.mock_stack_view.create_stack_element.call_count, len(self.fake_dict))

    def test_correct_dims_created(self):

        expected_calls = []

        for key in self.fake_dict.keys():

            data = self.fake_dict[key].data

            if len(data.dims) > 1:
                for i in range(len(data.dims)):
                    expected_calls.append(mock.call(data.dims[i], data.shape[i]))


        stack_pres = StackPresenter(self.mock_stack_view, self.mock_dim_fact)
        stack_pres.set_dict(self.fake_dict)

        self.assertEqual(self.mock_dim_fact.create_widget.call_count, len(expected_calls))
        self.mock_dim_fact.create_widget.assert_has_calls(expected_calls)
        self.assertEqual(self.mock_dim_widget.get_presenter.call_count, len(expected_calls))
