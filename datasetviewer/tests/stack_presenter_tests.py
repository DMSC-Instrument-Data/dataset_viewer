import unittest
from unittest import mock

from datasetviewer.stack.StackPresenter import StackPresenter
from datasetviewer.stack.interfaces.StackViewInterface import StackViewInterface
from datasetviewer.dimension.interfaces.DimensionViewFactoryInterface import DimensionViewFactoryInterface
from datasetviewer.dimension.interfaces.DimensionViewInterface import DimensionViewInterface
from datasetviewer.dimension.interfaces.DimensionPresenterInterface import DimensionPresenterInterface
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

        self.first_key = list(self.fake_dict.keys())[0]

        '''
        Find the expected number of calls that will be made to the DimensionViewFactory create_widget method for the
        above dictionary.
        '''
        self.expected_factory_call_count = 0

        for key in self.fake_dict.keys():
            data = self.fake_dict[key].data
            if len(data.dims) > 1:
                for i in range(len(data.dims)):
                    self.expected_factory_call_count += 1

        # Create mock DimensionView widgets to imitate the widget-creation sequence for the fake dictionary
        self.mock_dim_widgets = [mock.create_autospec(DimensionViewInterface)
                                 for _ in range(self.expected_factory_call_count)]

        # Instruct the mock DimensionViewFactory to return the mock widgets
        self.mock_dim_fact.create_widget = mock.MagicMock(side_effect = self.mock_dim_widgets)

        # Create mock DimensionPresenters and have them be returned by the mock DimensionViews
        self.mock_dim_presenters = [mock.create_autospec(DimensionPresenterInterface)
                                    for _ in range(self.expected_factory_call_count)]

        for i in range(self.expected_factory_call_count):
            self.mock_dim_widgets[i].get_presenter = mock.MagicMock(return_value=self.mock_dim_presenters[i])

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
        ''' Test that the stack is cleared whenever it received new data. '''

        stack_pres = StackPresenter(self.mock_stack_view, self.mock_dim_fact)
        stack_pres.set_dict(self.fake_dict)

        self.mock_stack_view.clear_stack.assert_called_once()

    def test_correct_stacks_created(self):
        ''' Test that the number of stacks created upon receiving new data matches the number of elements in the data
        dictionary. '''

        stack_pres = StackPresenter(self.mock_stack_view, self.mock_dim_fact)
        stack_pres.set_dict(self.fake_dict)

        expected_calls = [mock.call(key) for key in self.fake_dict.keys()]

        self.mock_stack_view.create_stack_element.assert_has_calls(expected_calls)
        self.assertEqual(self.mock_stack_view.create_stack_element.call_count, len(self.fake_dict))

    def test_correct_dims_created(self):
        ''' Test that the function for generating the dimension widgets makes the correct calls the correct number
        of times and with the correct arguments. This needs to be one call for every dimension in the entire
        dictionary minus the 1D datasets. '''

        expected_factory_calls = []

        for key in self.fake_dict.keys():

            fake_data = self.fake_dict[key].data

            # Skip data 1D data as it will not require dimension widgets
            if len(fake_data.dims) > 1:

                for i in range(len(fake_data.dims)):

                    # Create a mock call with the dimension name and size
                    expected_factory_calls.append(mock.call(fake_data.dims[i], fake_data.shape[i]))

        stack_pres = StackPresenter(self.mock_stack_view, self.mock_dim_fact)
        stack_pres.set_dict(self.fake_dict)

        # Check that the DimensionViewFactory received the expected calls and the expected number of calls
        self.mock_dim_fact.create_widget.assert_has_calls(expected_factory_calls)
        self.assertEqual(self.mock_dim_fact.create_widget.call_count, self.expected_factory_call_count)

    def test_get_dim_presenter(self):
        ''' Test that a presenter is retrieved from all of the mock widgets that are created by the
        DimensionViewFactory '''

        stack_pres = StackPresenter(self.mock_stack_view, self.mock_dim_fact)
        stack_pres.set_dict(self.fake_dict)

        for w in self.mock_dim_widgets:
            w.get_presenter.assert_called_once()

    def test_add_dimension_view_to_stack(self):
        ''' Test that the DimensionView is added to the correct index in the Stack '''

        stack_pres = StackPresenter(self.mock_stack_view, self.mock_dim_fact)
        stack_pres.set_dict(self.fake_dict)

        mock_add_dims_calls = []

        mock_dim_view_idx = 0

        for key in self.fake_dict.keys():

            fake_data = self.fake_dict[key].data

            if len(fake_data.dims) > 1:
                for _ in range(len(fake_data.dims)):
                    mock_add_dims_calls.append(mock.call(key,self.mock_dim_widgets[mock_dim_view_idx]))
                    mock_dim_view_idx += 1

        self.mock_stack_view.add_dimension_view.assert_has_calls(mock_add_dims_calls)
        self.assertEqual(self.mock_stack_view.add_dimension_view.call_count, self.expected_factory_call_count)

    def test_call_to_button_and_face(self):
        ''' Test that creating a default plot leads to a call to the function that creates the appropriate button
        configuration for the default plot. '''

        stack_pres = StackPresenter(self.mock_stack_view, self.mock_dim_fact)
        stack_pres.create_default_button_press = mock.Mock()
        stack_pres.change_stack_face = mock.Mock()

        stack_pres.set_dict(self.fake_dict)
        stack_pres.create_default_button_press.assert_called_once()
        stack_pres.change_stack_face.assert_called_once_with(self.first_key)

    def test_default_no_button_press(self):
        ''' Test that the correct buttons are pressed on the View in order to match the configuration of the default
        plot. '''

        stack_pres = StackPresenter(self.mock_stack_view, self.mock_dim_fact)

        # Create a dictionary for which the first element is 1D
        first_onedim = DataSet()
        first_onedim["onedim"] = self.fake_dict["onedim"]
        first_onedim["twodims"] = self.fake_dict["twodims"]

        # Send the dictionary to the mock StackPresenter
        stack_pres.set_dict(first_onedim)

        # Check that no buttons were pressed (this must happen as a 1D data will have no buttons anyway)
        self.mock_stack_view.press_x.assert_not_called()
        self.mock_stack_view.press_y.assert_not_called()

    def test_default_single_button_press(self):

        stack_pres = StackPresenter(self.mock_stack_view, self.mock_dim_fact)

        # Create a dictionary for which the first element is 2D
        first_twodim = DataSet()
        first_twodim["twodims"] = self.fake_dict["twodims"]
        first_twodim["onedim"] = self.fake_dict["onedim"]
        x_button_to_press = self.fake_dict["twodims"].data.dims[0]

        # Send the dictionary to the mock StackPresenter
        stack_pres.set_dict(first_twodim)

        # Check that just the X button has been pressed for the first dimension
        self.mock_stack_view.press_x.assert_called_once_with("twodims", x_button_to_press)
        self.mock_stack_view.press_y.assert_not_called()

    def test_default_two_button_press(self):

        stack_pres = StackPresenter(self.mock_stack_view, self.mock_dim_fact)

        # Create a dictionary for which the first element is 2D
        first_threedim = DataSet()
        first_threedim["threedims"] = self.fake_dict["threedims"]
        first_threedim["onedim"] = self.fake_dict["onedim"]
        x_button_to_press = self.fake_dict["threedims"].data.dims[0]
        y_button_to_press = self.fake_dict["threedims"].data.dims[1]

        # Send the dictionary to the mock StackPresenter
        stack_pres.set_dict(first_threedim)

        # Check that just the X button has been pressed for the first dimension
        self.mock_stack_view.press_x.assert_called_once_with("threedims", x_button_to_press)
        self.mock_stack_view.press_y.assert_called_once_with("threedims", y_button_to_press)

    def test_change_stack_face(self):
        ''' Test the change of the Stack face once a different element on the Preview has been selected. '''

        stack_pres = StackPresenter(self.mock_stack_view, self.mock_dim_fact)
        stack_pres.set_dict(self.fake_dict)

        self.mock_stack_view.change_stack_face.assert_called_once_with(self.first_key)

    def test_call_to_register_master(self):
        ''''''
        stack_pres = StackPresenter(self.mock_stack_view, self.mock_dim_fact)
        stack_pres.set_dict(self.fake_dict)

        for pres in self.mock_dim_presenters:
            pres.register_stack_master.assert_called_once_with(stack_pres)

    def test_y_button_press_counts_all_presses(self):

        stack_pres = StackPresenter(self.mock_stack_view, self.mock_dim_fact)
        stack_pres.set_dict(self.fake_dict)

        stack_pres._dims_with_x_pressed = mock.MagicMock()
        stack_pres._dims_with_y_pressed = mock.MagicMock()

        stack_pres.y_button_press('y', True)
        stack_pres._dims_with_x_pressed.assert_called_once()
        stack_pres._dims_with_y_pressed.assert_called_once()
