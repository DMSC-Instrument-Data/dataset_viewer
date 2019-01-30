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
        Find the expected number of calls that will be made to the DimensionViewFactory create_widgets method for the
        above dictionary. This is equal to the total number of dimensions for all datasets that have at least two
        dimensions.
        '''
        self.expected_factory_call_count = 0

        # Prepare a Stack counter to mimic the behaviour of the Stack creation
        stack_counter = 0

        self.mock_dim_widgets = DataSet()
        self.mock_dim_presenters = DataSet()
        self.stack_idx = {}

        for key in self.fake_dict.keys():

            data = self.fake_dict[key].data
            self.stack_idx[key] = stack_counter
            stack_counter += 1

            if len(data.dims) > 1:

                for i in range(len(data.dims)):

                    self.expected_factory_call_count += 1

                    mock_dim_presenter = mock.create_autospec(DimensionPresenterInterface)
                    self.mock_dim_presenters[data.dims[i]] = mock_dim_presenter

                    self.mock_dim_widgets[data.dims[i]] = mock.create_autospec(DimensionViewInterface)
                    self.mock_dim_widgets[data.dims[i]].get_presenter = mock.MagicMock(return_value = mock_dim_presenter)

        # Instruct the mock DimensionViewFactory to return the mock widgets
        self.mock_dim_fact.create_widgets = mock.MagicMock(side_effect = lambda name, shape: self.mock_dim_widgets[name])
        self.mock_stack_view.create_stack_element = mock.MagicMock(side_effect = [i for i in range(len(self.fake_dict.keys()))])
        self.mock_stack_view.count = mock.MagicMock(return_value = len(self.fake_dict.keys()))

    def test_presenter_throws_if_args_none(self):
        ''' Test that exceptions are thrown if the DimensionViewFactory or StackView are None. '''

        with self.assertRaises(ValueError):
            StackPresenter(None, self.mock_dim_fact)

        with self.assertRaises(ValueError):
            StackPresenter(self.mock_stack_view, None)

    def test_register_master(self):
        ''' Test the two-way relationship between the StackPresenter and the MainViewPresenter. '''

        stack_pres = StackPresenter(self.mock_stack_view, self.mock_dim_fact)
        stack_pres.register_master(self.mock_main_presenter)

        self.mock_main_presenter.subscribe_stack_presenter.assert_called_once_with(stack_pres)

    def test_correct_stacks_created(self):
        ''' Test that the number of stacks created upon receiving new data matches the number of elements in the data
        dictionary. '''

        stack_pres = StackPresenter(self.mock_stack_view, self.mock_dim_fact)
        stack_pres.set_dict(self.fake_dict)

        self.assertEqual(self.mock_stack_view.create_stack_element.call_count, len(self.fake_dict))

    def test_correct_dims_created(self):
        ''' Test that the function for generating the dimension widgets makes the correct calls the correct number
        of times. This needs to be one call for every dimension in the entire dictionary minus the 1D datasets. '''

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
        self.mock_dim_fact.create_widgets.assert_has_calls(expected_factory_calls)
        self.assertEqual(self.mock_dim_fact.create_widgets.call_count, self.expected_factory_call_count)

    def test_get_dim_presenter(self):
        ''' Test that a presenter is retrieved from all of the mock widgets that are created by the
        DimensionViewFactory '''

        stack_pres = StackPresenter(self.mock_stack_view, self.mock_dim_fact)
        stack_pres.set_dict(self.fake_dict)

        for w in self.mock_dim_widgets.values():
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
                for i in range(len(fake_data.dims)):
                    mock_add_dims_calls.append(mock.call(self.stack_idx[key],self.mock_dim_widgets[fake_data.dims[i]]))
                    mock_dim_view_idx += 1

        # self.mock_stack_view.add_dimension_widget.assert_has_calls(mock_add_dims_calls)
        # self.assertEqual(self.mock_stack_view.add_dimension_view.call_count, self.expected_factory_call_count)

    def test_call_to_button_and_face(self):
        ''' Test that creating a default plot leads to a call to the function that creates the appropriate button
        configuration for the default plot. '''

        stack_pres = StackPresenter(self.mock_stack_view, self.mock_dim_fact)
        stack_pres.create_default_button_press = mock.Mock()
        stack_pres.change_stack_face = mock.Mock()

        stack_pres.set_dict(self.fake_dict)
        stack_pres.change_stack_face.assert_called_once_with(self.first_key)

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
        self.mock_dim_presenters[x_button_to_press].set_x_state.assert_called_once_with(True)
        # self.mock_dim_presenters[x_button_to_press].set_y_state.assert_called_once_with(False)
        self.mock_dim_presenters[x_button_to_press].disable_dimension.assert_called_once()

        # Check that the buttons have been released for the other dimensions
        for dim in self.fake_dict["twodims"].data.dims:

            if dim == x_button_to_press:
                continue

            self.mock_dim_presenters[dim].enable_dimension.assert_called_once()

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
        self.mock_dim_presenters[x_button_to_press].set_x_state.assert_called_once_with(True)
        self.mock_dim_presenters[x_button_to_press].disable_dimension.assert_called_once()

        self.mock_dim_presenters[y_button_to_press].set_y_state.assert_called_once_with(True)
        self.mock_dim_presenters[y_button_to_press].disable_dimension.assert_called_once()

    def test_change_stack_face(self):
        ''' Test the change of the Stack face once a different element on the Preview has been selected. '''

        stack_pres = StackPresenter(self.mock_stack_view, self.mock_dim_fact)
        stack_pres.set_dict(self.fake_dict)

        self.mock_stack_view.change_stack_face.assert_called_once_with(self.stack_idx[self.first_key])

    def test_call_to_register_master(self):
        ''' Test that the DimensionPresenters are assigned the StackPresenter as master after their creation. '''

        stack_pres = StackPresenter(self.mock_stack_view, self.mock_dim_fact)
        stack_pres.set_dict(self.fake_dict)

        for pres in self.mock_dim_presenters.values():
            pres.register_stack_master.assert_called_once_with(stack_pres)

    def test_no_x_buttons_pressed(self):

        # Have the DimensionPresenters say that their X buttons are unchecked
        for p in self.mock_dim_presenters.values():
            p.get_x_state = mock.MagicMock(return_value=False)

        stack_pres = StackPresenter(self.mock_stack_view, self.mock_dim_fact)
        stack_pres.set_dict(self.fake_dict)

        self.assertEqual(stack_pres._dims_with_x_checked(), set())

    def test_no_y_buttons_pressed(self):

        # Have the DimensionPresenters say that their Y buttons are unchecked
        for p in self.mock_dim_presenters.values():
            p.get_y_state = mock.MagicMock(return_value=False)

        stack_pres = StackPresenter(self.mock_stack_view, self.mock_dim_fact)
        stack_pres.set_dict(self.fake_dict)

        self.assertEqual(stack_pres._dims_with_y_checked(), set())

    def test_single_x_button_changed(self):

        # Have the DimensionPresenters say that their X buttons are unchecked
        for p in self.mock_dim_presenters.values():
            p.get_x_state = mock.MagicMock(return_value=False)

        # Set the Presenter that corresponds with element "threedims", dimension "z" report that its X button is checked
        self.mock_dim_presenters['z'].get_x_state = mock.MagicMock(return_value = True)

        stack_pres = StackPresenter(self.mock_stack_view, self.mock_dim_fact)
        stack_pres.set_dict(self.fake_dict)

        self.assertEqual(stack_pres._dims_with_x_checked(), {'z'})

    def test_single_y_button_changed(self):

        # Have the DimensionPresenters say that their Y buttons are unchecked
        for p in self.mock_dim_presenters.values():
            p.get_y_state = mock.MagicMock(return_value=False)

        # Set the Presenter that corresponds with element "threedims", dimension "z" report that its Y button is checked
        self.mock_dim_presenters['z'].get_y_state = mock.MagicMock(return_value = True)

        stack_pres = StackPresenter(self.mock_stack_view, self.mock_dim_fact)
        stack_pres.set_dict(self.fake_dict)

        self.assertEqual(stack_pres._dims_with_y_checked(), {'z'})

    def test_uncheck_y_creates_onedim_plot(self):

        # Have the DimensionPresenters say that their X and Y buttons are unchecked
        for p in self.mock_dim_presenters.values():
            p.get_x_state = mock.MagicMock(return_value=False)
            p.get_y_state = mock.MagicMock(return_value=False)

        # Create fake slider values for the two dimensions in the first element of the dataset
        self.mock_dim_presenters['x'].get_slider_value = mock.MagicMock(return_value = 8)
        self.mock_dim_presenters['y'].get_slider_value = mock.MagicMock(return_value = 5)

        # Create the slice dictionary that matches the fake slider values
        slice = {'x': 8, 'y': 5}

        # Tell the Presenter that corresponds with dimension 'z' to report that its X button is checked
        self.mock_dim_presenters['z'].get_x_state = mock.MagicMock(return_value = True)
        self.mock_dim_presenters['z'].is_enabled = mock.MagicMock(return_value = False)

        stack_pres = StackPresenter(self.mock_stack_view, self.mock_dim_fact)
        stack_pres.register_master(self.mock_main_presenter)
        stack_pres.set_dict(self.fake_dict)

        # Send the instruction to uncheck the Y button for dimension 'x'
        stack_pres.y_button_change('x', False)

        # Check that this causes the slider and stepper buttons to reappear for the 'x' dimension
        self.mock_dim_presenters['x'].enable_dimension.assert_called_once()

        # Check that this causes the master to create a one-dimensional plot with the correct arguments
        self.mock_main_presenter.create_onedim_plot.assert_called_once_with("threedims",    # The key of the dataset
                                                                            'z',            # The x dimension
                                                                            slice)          # The slice dictionary

    def test_check_y_goes_to_twodim_from_onedim(self):

        # Have the DimensionPresenters say that their X and Y buttons are unchecked
        for p in self.mock_dim_presenters.values():
            p.get_x_state = mock.MagicMock(return_value=False)
            p.get_y_state = mock.MagicMock(return_value=False)

        # Create fake slider values for a single dimension in the first element of the dataset
        self.mock_dim_presenters['x'].get_slider_value = mock.MagicMock(return_value = 8)

        # Create the slice dictionary that matches the fake slider values
        slice = {'x': 8}

        # Tell the Presenter that corresponds with dimension 'y' to report that its X button is checked
        self.mock_dim_presenters['y'].get_x_state = mock.MagicMock(return_value = True)
        self.mock_dim_presenters['y'].is_enabled = mock.MagicMock(return_value = False)

        '''
        Tell the Presenter that corresponds with dimension 'z' to report that its Y button has recently been checked
        but has yet been disabled
        '''
        self.mock_dim_presenters['z'].get_y_state = mock.MagicMock(return_value = True)
        self.mock_dim_presenters['z'].is_enabled = mock.MagicMock(return_value = True)

        def mock_z_disable():
            self.mock_dim_presenters['z'].is_enabled = mock.MagicMock(return_value=False)

        # Create a mock for `enable_dimension` so that the 'y' Presenter can behave as if its button has been enabled
        self.mock_dim_presenters['z'].disable_dimension = mock.MagicMock(side_effect = mock_z_disable)

        stack_pres = StackPresenter(self.mock_stack_view, self.mock_dim_fact)
        stack_pres.register_master(self.mock_main_presenter)
        stack_pres.set_dict(self.fake_dict)

        # Send the instruction to check the Y button for dimension 'z'
        stack_pres.y_button_change('z', True)

        # Check that this causes the slider and stepper buttons to disappear for the 'z' dimension
        self.mock_dim_presenters['z'].disable_dimension.assert_called_once()

        # Check that this causes the master to create a two-dimensional plot with the correct arguments
        self.mock_main_presenter.create_twodim_plot.assert_called_once_with("threedims", # The dataset to plot/slice
                                                                            'y',         # The x dimension
                                                                            'z',         # The y dimension
                                                                            slice)       # The slice dictionary

    def test_check_change_y_creates_new_twodim_plot(self):

        # Have the DimensionPresenters say that their X and Y buttons are unchecked
        for p in self.mock_dim_presenters.values():
            p.get_x_state = mock.MagicMock(return_value=False)
            p.get_y_state = mock.MagicMock(return_value=False)

        # Create fake slider values for a single dimension in the first element of the dataset
        self.mock_dim_presenters['x'].get_slider_value = mock.MagicMock(return_value = 2)

        # Create the slice dictionary that matches the fake slider values
        slice = {'x': 2}

        # Tell the Presenter that corresponds with dimension 'y' to report that its X button is checked
        self.mock_dim_presenters['y'].get_x_state = mock.MagicMock(return_value = True)
        self.mock_dim_presenters['y'].is_enabled = mock.MagicMock(return_value = False)

        # Tell the Presenter that corresponds with dimension 'x to report that its Y button is checked
        self.mock_dim_presenters['x'].get_y_state = mock.MagicMock(return_value = True)
        self.mock_dim_presenters['x'].is_enabled = mock.MagicMock(return_value = False)

        '''
        Tell the Presenter that corresponds with dimension 'z' to report that its Y button has recently been pressed,
        but that it has not yet been disabled
        '''
        self.mock_dim_presenters['z'].get_y_state = mock.MagicMock(return_value = True)
        self.mock_dim_presenters['z'].is_enabled = mock.MagicMock(return_value = True)

        def mock_z_disable():
            self.mock_dim_presenters['z'].is_enabled = mock.MagicMock(return_value = False)

        # Create a mock for `enable_dimension` so that the 'y' Presenter can behave as if its button has been enabled
        self.mock_dim_presenters['z'].disable_dimension = mock.MagicMock(side_effect = mock_z_disable)

        def mock_x_enable():
            self.mock_dim_presenters['x'].is_enabled = mock.MagicMock(return_value = True)

        # Create a mock for `enable_dimension` so that the 'y' Presenter can behave as if its button has been enabled
        self.mock_dim_presenters['x'].enable_dimension = mock.MagicMock(side_effect= mock_x_enable)

        stack_pres = StackPresenter(self.mock_stack_view, self.mock_dim_fact)
        stack_pres.register_master(self.mock_main_presenter)
        stack_pres.set_dict(self.fake_dict)

        # Send the instruction to check the Y button for dimension 'z'
        stack_pres.y_button_change('z', True)

        # Check that this causes the slider and stepper buttons to disappear for the 'z' dimension
        self.mock_dim_presenters['z'].disable_dimension.assert_called_once()

        # Check that this causes the slider and stepper buttons to reappear for the 'x' dimension
        self.mock_dim_presenters['x'].enable_dimension.assert_called_once()

        # Check that this causes the master to create a two-dimensional plot with the correct arguments
        self.mock_main_presenter.create_twodim_plot.assert_called_once_with("threedims",    # The key of the dataset
                                                                            'y',            # The x dimension
                                                                            'z',            # The y dimension
                                                                            slice)          # The slice dictionary

    def test_change_onedim_plot(self):

        # Have the DimensionPresenters say that their X and Y buttons are unchecked
        for p in self.mock_dim_presenters.values():
            p.get_x_state = mock.MagicMock(return_value=False)
            p.get_y_state = mock.MagicMock(return_value=False)

        # Create fake slider values for two dimensions in the first element of the dataset
        self.mock_dim_presenters['x'].get_slider_value = mock.MagicMock(return_value = 1)
        self.mock_dim_presenters['y'].get_slider_value = mock.MagicMock(return_value = 6)

        # Create the slice dictionary that matches the fake slider values
        slice = {'x': 1, 'y': 6}

        # Set the DimensionPresenter for the 'y' dimension to report that it's disabled and its X button is checked
        self.mock_dim_presenters['y'].is_enabled = mock.MagicMock(return_value = False)
        self.mock_dim_presenters['y'].get_x_state = mock.MagicMock(return_value = True)

        def mock_y_enable():
            self.mock_dim_presenters['y'].is_enabled = mock.MagicMock(return_value = True)

        # Create a mock for `enable_dimension` so that the 'y' Presenter can behave as if its button has been enabled
        self.mock_dim_presenters['y'].enable_dimension = mock.MagicMock(side_effect = mock_y_enable)

        '''
        Set the DimensionPresenter for the 'z' dimension to report that its X button is checked but that it has not yet
        been disabled. This matches the conditions of a recent button push that hasn't yet been interpreted by the
        StackPresenter. Once this button push is accepted we expect the StackPresenter to disable this Dimension.
        '''
        self.mock_dim_presenters['z'].is_enabled = mock.MagicMock(return_value = True)
        self.mock_dim_presenters['z'].get_x_state = mock.MagicMock(return_value = True)

        def mock_z_disable():
            self.mock_dim_presenters['z'].is_enabled = mock.MagicMock(return_value = False)

        # Create a mock for `disable_dimension` so that the 'z' Presenter can behave as if it's been disabled
        self.mock_dim_presenters['z'].disable_dimension = mock.MagicMock(side_effect = mock_z_disable)

        stack_pres = StackPresenter(self.mock_stack_view, self.mock_dim_fact)
        stack_pres.register_master(self.mock_main_presenter)
        stack_pres.set_dict(self.fake_dict)

        # Send the instruction to check the Y button for dimension 'z'
        stack_pres.x_button_change('z', True)

        # Check that the 'y' dimension was disabled and that 'z' dimension was disabled
        self.mock_dim_presenters['y'].enable_dimension.assert_called_once()
        self.mock_dim_presenters['z'].disable_dimension.assert_called_once()

        # Check that the function for creating a 1D plot was called with the expected arguments
        self.mock_main_presenter.create_onedim_plot.assert_called_once_with("threedims",    # The key of the dataset
                                                                            'z',            # The x dimension
                                                                            slice)          # The slice dictionary

    def test_press_x_changes_twodim_plot(self):
        '''Test that selecting an X button when another X button and Y button have already be pressed causes the
        previous X button to be released and instructs the MainViewPresenter to change the dimensions of the 2D plot.'''

        # Have the DimensionPresenters say that their X and Y buttons are unchecked
        for p in self.mock_dim_presenters.values():
            p.get_x_state = mock.MagicMock(return_value=False)
            p.get_y_state = mock.MagicMock(return_value=False)

        # Create fake slider values for a single dimension in the first element of the dataset
        self.mock_dim_presenters['z'].get_slider_value = mock.MagicMock(return_value = 3)

        # Create the slice dictionary that matches the fake slider values
        slice = {'z': 3}

        # Instruct the mock Presenter for 'z' to report that its disabled and its X button is checked
        self.mock_dim_presenters['z'].is_enabled = mock.MagicMock(return_value = False)
        self.mock_dim_presenters['z'].get_x_state = mock.MagicMock(return_value = True)

        def mock_z_enable():
            self.mock_dim_presenters['z'].is_enabled = mock.MagicMock(return_value = True)

        # Create a mock for `enable_dimension` so that the 'z' Presenter can behave as if it's been enabled
        self.mock_dim_presenters['z'].enable_dimension = mock.MagicMock(side_effect = mock_z_enable)

        '''
        Set the DimensionPresenter for the 'y' dimension to report that it's enabled and its X button is checked. This
        matches the conditions of a recent button push that hasn't yet been interpreted by the StackPresenter. Once
        this button push is accepted we expect the StackPresenter to disable this Dimension.
        '''
        self.mock_dim_presenters['y'].is_enabled = mock.MagicMock(return_value = True)
        self.mock_dim_presenters['y'].get_x_state = mock.MagicMock(return_value = True)

        def mock_y_disable():
            self.mock_dim_presenters['y'].is_enabled = mock.MagicMock(return_value = False)

        # Create a mock for `disable_dimension` so that the 'y' Presenter can behave as if it's been disabled
        self.mock_dim_presenters['y'].disable_dimension = mock.MagicMock(side_effect = mock_y_disable)

        # Have the mock for the 'x' Presenter report that it's disabled and its Y button is checked
        self.mock_dim_presenters['x'].is_enabled = mock.MagicMock(return_value = False)
        self.mock_dim_presenters['x'].get_y_state = mock.MagicMock(return_value = True)

        stack_pres = StackPresenter(self.mock_stack_view, self.mock_dim_fact)
        stack_pres.register_master(self.mock_main_presenter)
        stack_pres.set_dict(self.fake_dict)

        # Reset the mocks so that we ignore the function calls made in `set_dict`
        self.mock_dim_presenters['z'].reset_mock()
        self.mock_dim_presenters['y'].reset_mock()

        # Send the instruction to check the X button for dimension 'y'
        stack_pres.x_button_change('y', True)

        # Check that pressing the new X button causes the previous X (dimension 'z') to be released
        self.mock_dim_presenters['z'].enable_dimension.assert_called_once()

        # Check that the new X (dimension 'y') has not been disabled
        self.mock_dim_presenters['y'].disable_dimension.assert_called_once()

        # Check that a call to `create_twodim_plot` is made with the correct arguments
        self.mock_main_presenter.create_twodim_plot.assert_called_once_with("threedims", # The key of the dataset
                                                                            'y',         # The x dimension
                                                                            'x',         # The y dimension
                                                                            slice)       # The slice dictionary

    def test_x_wrong_number_buttons_pressed_throws(self):
        ''' Test that the `x_button_change` function throws an exception when an incorrect number of X/Y buttons have
        been pressed. '''

        stack_pres = StackPresenter(self.mock_stack_view, self.mock_dim_fact)
        stack_pres.register_master(self.mock_main_presenter)
        stack_pres.set_dict(self.fake_dict)

        # Make the DimensionPresenters report that every X button has been pressed
        for p in self.mock_dim_presenters.values():
            p.get_x_state = mock.MagicMock(return_value=True)
            p.get_y_state = mock.MagicMock(return_value=False)

        with self.assertRaises(ValueError):
            stack_pres.x_button_change('x', True)

        # Make the DimensionPresenters report that no X buttons have been pressed
        for p in self.mock_dim_presenters.values():
            p.get_x_state = mock.MagicMock(return_value=False)
            p.get_y_state = mock.MagicMock(return_value=False)

        # Create one Y press so we know the X buttons are the source of the problem
        self.mock_dim_presenters['x'].get_y_state = mock.MagicMock(return_Value = True)

        with self.assertRaises(ValueError):
            stack_pres.x_button_change('x', True)

        # Make the DimensionPresenters report that every Y button has been pressed
        for p in self.mock_dim_presenters.values():
            p.get_x_state = mock.MagicMock(return_value=False)
            p.get_y_state = mock.MagicMock(return_value=True)

        # Create one X press so that we know the Y buttons are the source of the problem
        self.mock_dim_presenters['x'].get_x_state = mock.MagicMock(return_Value=True)

        with self.assertRaises(ValueError):
            stack_pres.x_button_change('x', True)

    def test_y_wrong_number_buttons_pressed_throws(self):
        ''' Test that the `y_button_change` function throws an exception when an incorrect number of X/Y buttons have
        been pressed. '''

        stack_pres = StackPresenter(self.mock_stack_view, self.mock_dim_fact)
        stack_pres.register_master(self.mock_main_presenter)
        stack_pres.set_dict(self.fake_dict)

        # Make the DimensionPresenters report that every X button has been pressed
        for p in self.mock_dim_presenters.values():
            p.get_x_state = mock.MagicMock(return_value=True)
            p.get_y_state = mock.MagicMock(return_value=False)

        with self.assertRaises(ValueError):
            stack_pres.y_button_change('x', True)

        # Make the DimensionPresenters report that no X buttons have been pressed
        for p in self.mock_dim_presenters.values():
            p.get_x_state = mock.MagicMock(return_value=False)
            p.get_y_state = mock.MagicMock(return_value=False)

        # Create one Y press so we know the X buttons are the source of the problem
        self.mock_dim_presenters['x'].get_y_state = mock.MagicMock(return_Value=True)

        with self.assertRaises(ValueError):
            stack_pres.y_button_change('x', True)

        # Make the DimensionPresenters report that every Y button has been pressed
        for p in self.mock_dim_presenters.values():
            p.get_x_state = mock.MagicMock(return_value=False)
            p.get_y_state = mock.MagicMock(return_value=True)

        # Create one X press so we know the Y buttons are the source of the problem
        self.mock_dim_presenters['x'].get_x_state = mock.MagicMock(return_Value=True)

        with self.assertRaises(ValueError):
            stack_pres.y_button_change('x', True)

    def test_slice_change_onedim_plot(self):
        ''' Test that the correct functions calls are made when a slider/stepper is changed in the case of a 1D plot.'''

        stack_pres = StackPresenter(self.mock_stack_view, self.mock_dim_fact)
        stack_pres.register_master(self.mock_main_presenter)
        stack_pres.set_dict(self.fake_dict)

        # Make the DimensionPresenters report that the 'x' dimension is the chosen X button
        self.mock_dim_presenters['x'].get_x_state = mock.MagicMock(return_value = True)
        self.mock_dim_presenters['x'].get_y_state = mock.MagicMock(return_value=False)
        self.mock_dim_presenters['x'].is_enabled = mock.MagicMock(return_value = False)

        # Make the DimensionPresenters report that the 'y' and 'z'  dimension are enabled and have no checked buttons
        self.mock_dim_presenters['y'].get_x_state = mock.MagicMock(return_value=False)
        self.mock_dim_presenters['y'].get_y_state = mock.MagicMock(return_value=False)
        self.mock_dim_presenters['y'].is_enabled = mock.MagicMock(return_value=True)
        self.mock_dim_presenters['z'].get_x_state = mock.MagicMock(return_value=False)
        self.mock_dim_presenters['z'].get_y_state = mock.MagicMock(return_value=False)
        self.mock_dim_presenters['z'].is_enabled = mock.MagicMock(return_value=True)

        # Also provide fake slider values for the mock DimensionPresenters that have no buttons pressed
        self.mock_dim_presenters['y'].get_slider_value = mock.MagicMock(return_value = 2)
        self.mock_dim_presenters['z'].get_slider_value = mock.MagicMock(return_value = 11)

        # Generate the expected dictionary for this slice
        slice = {'y': 2, 'z': 11}

        '''
        Call the slice change function with the current DimensionPresenter setup. This should cause the StackPresenter
        to inform the MainPresenter to generate a 1D plot as only a single X button has been selected.
        '''
        stack_pres.slice_change()

        self.mock_main_presenter.create_onedim_plot.assert_called_once_with("threedims",
                                                                            'x',
                                                                            slice)
    def test_slice_change_twodim_plot(self):
        ''' Test that the correct functions calls are made when a slider/stepper is changed in the case of a  1D plot'''

        stack_pres = StackPresenter(self.mock_stack_view, self.mock_dim_fact)
        stack_pres.register_master(self.mock_main_presenter)
        stack_pres.set_dict(self.fake_dict)

        # Make the DimensionPresenters report that the 'x' dimension is the chosen X button
        self.mock_dim_presenters['x'].get_x_state = mock.MagicMock(return_value = True)
        self.mock_dim_presenters['x'].get_y_state = mock.MagicMock(return_value=False)
        self.mock_dim_presenters['x'].is_enabled = mock.MagicMock(return_value = False)

        # Make the DimensionPresenters report that the 'y' dimension is the chosen Y button
        self.mock_dim_presenters['y'].get_x_state = mock.MagicMock(return_value=False)
        self.mock_dim_presenters['y'].get_y_state = mock.MagicMock(return_value=True)
        self.mock_dim_presenters['y'].is_enabled = mock.MagicMock(return_value=False)

        # Make the DimensionPresenter report that the 'z' dimension is unchecked and its slider has value 11
        self.mock_dim_presenters['z'].get_x_state = mock.MagicMock(return_value=False)
        self.mock_dim_presenters['z'].get_y_state = mock.MagicMock(return_value=False)
        self.mock_dim_presenters['z'].is_enabled = mock.MagicMock(return_value=True)
        self.mock_dim_presenters['z'].get_slider_value = mock.MagicMock(return_value = 11)

        # Generate the expected dictionary for this slice
        slice = {'z': 11}

        '''
        Call the slice change function with the current DimensionPresenter setup. This should cause the StackPresenter
        to inform the MainPresenter to generate a 2D plot as both an X and Y button have been selected.
        '''
        stack_pres.slice_change()

        self.mock_main_presenter.create_twodim_plot.assert_called_once_with("threedims",    # The key of the dataset
                                                                            'x',            # The x dimension
                                                                            'y',            # The y dimension
                                                                            slice)          # The slice dictionary

    def clear_stack_test(self):
        ''' Test that the clear stack function makes the expected calls to the StackView.'''

        stack_pres = StackPresenter(self.mock_stack_view, self.mock_dim_fact)
        stack_pres.register_master(self.mock_main_presenter)

        # By setting this data we create four elements on the StackView for the four datasets
        stack_pres.set_dict(self.fake_dict)

        # Dismiss the first call made to `clear_stack` upon data loading
        self.mock_stack_view.reset_mock()
        stack_pres._clear_stack()

        stack_idxs = [3, 2, 1, 0]
        delete_widget_calls = []

        # Create mock calls consisting of the Stack indexes going from the largest index to the smallest
        for idx in stack_idxs:
            delete_widget_calls.append(mock.call(idx))

        # Check that the mock Stack view received identical calls to its `delete_widget` function
        self.mock_stack_view.delete_widget.assert_has_calls(delete_widget_calls)
        self.assertEqual(self.mock_stack_view.delete_widget.call_count, len(stack_idxs))

    def test_new_file_erases_previous_information(self):
        ''' Test that loading one dataset and then another dataset clears any previous information about presenters and
        indexes on the StackPresenter.'''

        stack_pres = StackPresenter(self.mock_stack_view, self.mock_dim_fact)
        stack_pres.register_master(self.mock_main_presenter)
        stack_pres.set_dict(self.fake_dict)

        new_dict = DataSet()
        new_dict["twodims"] = self.fake_dict["twodims"]
        new_dict["fourdims"] = self.fake_dict["fourdims"]

        self.mock_stack_view.create_stack_element = mock.MagicMock()

        # Call `set_dict` a second time with a different dataset
        stack_pres.set_dict(new_dict)

        # Check that the Stack index dictionary has the expected size
        self.assertEquals(len(stack_pres._stack_idx),len(new_dict.keys()))

        # Check that the Presenter dictionaries have the expected sizes
        self.assertEquals(len(stack_pres._dim_presenters), len(new_dict.keys()))
        self.assertEquals(len(stack_pres._dim_presenters["twodims"]), 2)
        self.assertEquals(len(stack_pres._dim_presenters["fourdims"]), 4)
