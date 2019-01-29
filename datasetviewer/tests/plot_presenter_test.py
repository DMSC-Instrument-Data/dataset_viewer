import unittest
import mock

import xarray as xr
import numpy as np

from datasetviewer.mainview.interfaces.MainViewPresenterInterface import MainViewPresenterInterface
from datasetviewer.plot.interfaces.PlotViewInterface import PlotViewInterface
from datasetviewer.plot.PlotPresenter import PlotPresenter

from collections import OrderedDict as DataSet
from datasetviewer.dataset.Variable import Variable

class PlotPresenterTest(unittest.TestCase):

    def setUp(self):

        self.mock_plot_view = mock.create_autospec(PlotViewInterface)

        self.mock_main_presenter = mock.create_autospec(MainViewPresenterInterface)

        # Create a fake data dictionary with valid elements
        self.fake_dict = DataSet()
        self.fake_dict["threedims"] = Variable("threedims", xr.DataArray(np.random.rand(3, 4, 5), dims=['x', 'y', 'z']))
        self.fake_dict["onedim"] = Variable("onedim", xr.DataArray(np.random.rand(3), dims=['b']))
        self.fake_dict["twodims"] = Variable("twodims", xr.DataArray(np.random.rand(3, 8), dims=['g', 'h']))
        self.fake_dict["fourdims"] = Variable("fourdims", xr.DataArray(np.random.rand(3, 4, 5, 6), dims=['c', 'd', 'e', 'f']))

    def test_presenter_throws_when_view_none(self):
        '''
        Test that the PlotPresenter throws an Exception when the PlotView is None.
        '''

        with self.assertRaises(ValueError):
            PlotPresenter(None)

    def test_clear_plot(self):
        '''
        Test that loading a new data array causes the previous plot to be cleared.
        '''

        plot_pres = PlotPresenter(self.mock_plot_view)
        plot_pres.register_master(self.mock_main_presenter)
        plot_pres._clear_plot = mock.MagicMock()
        plot_pres.set_dict(self.fake_dict)
        plot_pres._clear_plot.assert_called_once()

    def test_plot_call(self):
        '''
        Test that creating a default plot with nD data causes the appropriate plot function to be called in the
        PlotView.
        '''

        plot_pres = PlotPresenter(self.mock_plot_view)
        plot_pres.register_master(self.mock_main_presenter)
        plot_pres.set_dict(self.fake_dict)

        plot_pres.create_default_plot("onedim")
        xr.testing.assert_identical(self.mock_plot_view.plot_line.call_args[0][0], self.fake_dict["onedim"].data)

        plot_pres.create_default_plot("twodims")
        xr.testing.assert_identical(self.mock_plot_view.plot_line.call_args[0][0],
                                    self.fake_dict["twodims"].data.transpose()[0])

        plot_pres.create_default_plot("fourdims")
        xr.testing.assert_identical(self.mock_plot_view.plot_image.call_args[0][0],
                                    self.fake_dict["fourdims"].data.isel({'e':0, 'f':0}).transpose('d', 'c'))

    def test_register_master(self):
        '''
        Test the two-way link between the PlotPresenter and its MainViewPresenter by ensuring that the master's
        `subscribe_plot_presenter` method is called after the PlotPresenter's `register_master` method is called.
        '''

        plot_pres = PlotPresenter(self.mock_plot_view)
        plot_pres.register_master(self.mock_main_presenter)

        self.mock_main_presenter.subscribe_plot_presenter.assert_called_once_with(plot_pres)

    def test_label_axes(self):
        '''
        Test that the axes label functions are called with the expected inputs.
        '''

        # Don't label the axes in the case of 1D data
        plot_pres = PlotPresenter(self.mock_plot_view)
        plot_pres.register_master(self.mock_main_presenter)

        # Set the dict attribute directly to bypass the function calls in `set_dict`
        plot_pres._dict = self.fake_dict

        # Check that the axes aren't labelled when a 1D array has been plotted
        plot_pres.create_default_plot("onedim")
        self.mock_plot_view.label_x_axis.assert_not_called()
        self.mock_plot_view.label_y_axis.assert_not_called()

        # Label a single axes in the case of 2D data
        plot_pres.create_default_plot("twodims")
        self.mock_plot_view.label_x_axis.assert_called_once_with(self.fake_dict["twodims"].data.dims[0])
        self.mock_plot_view.label_y_axis.assert_not_called()

        self.mock_plot_view.reset_mock()
        plot_pres._dict = self.fake_dict

        # Label both axes in the case of nD data with n > 2
        plot_pres.create_default_plot("threedims")
        self.mock_plot_view.label_x_axis.assert_called_once_with(self.fake_dict["threedims"].data.dims[0])
        self.mock_plot_view.label_y_axis.assert_called_once_with(self.fake_dict["threedims"].data.dims[1])

    def test_update_plot(self):
        '''
        Test that calling `_update_plot` in the PlotPresenter causes the PlotView to redraw the plot and causes the
        MainPresenter to update the toolbar.
        '''

        self.mock_plot_view.draw_plot = mock.MagicMock()

        plot_pres = PlotPresenter(self.mock_plot_view)
        plot_pres.register_master(self.mock_main_presenter)
        plot_pres.set_dict(self.fake_dict)

        self.mock_plot_view.reset_mock()
        self.mock_main_presenter.reset_mock()

        plot_pres._update_plot()

        self.mock_plot_view.draw_plot.assert_called_once()
        self.mock_main_presenter.update_toolbar.assert_called_once()

    def test_create_onedim_plot(self):
        '''
        Test that calling the 1D plot function when given a dictionary key, a dimension, and a dictionary of slices
        creates the expected array and passes it to the PlotView.
        '''

        plot_pres = PlotPresenter(self.mock_plot_view)
        plot_pres.register_master(self.mock_main_presenter)
        plot_pres.set_dict(self.fake_dict)

        self.mock_plot_view.reset_mock()
        self.mock_main_presenter.reset_mock()

        '''
        Create fake parameters that correspond with a request to generate a 1D plot from the "threedims" dataset using
        'x' as the x-axis and slider/stepper values of 2 and 3 for the remaining dimensions.
        '''
        fake_key = "threedims"
        fake_x = 'x'
        fake_slice = {'y': 2, 'z': 3}

        plot_pres.create_onedim_plot(fake_key, fake_x, fake_slice)

        # Generate the expected sliced array from these parameters
        arr = self.fake_dict[fake_key].data.isel(fake_slice)

        '''
        Check for equality between the array that has just been created and the argument sent to the PlotView. This is
        done using xarray's built in equality function.
        '''
        self.assertTrue(arr.equals(self.mock_plot_view.plot_line.call_args[0][0]))

        # Check that the axis label has changed and the relevant plot elements are updated
        self.mock_plot_view.label_x_axis.assert_called_once_with(fake_x)
        self.mock_plot_view.draw_plot.assert_called_once()
        self.mock_main_presenter.update_toolbar.assert_called_once()

    def test_create_twodim_plot(self):
        '''
        Test that calling the 2D plot function when given a dictionary key, x and y dimensions, and a dictionary of
        slices creates the expected array and passes it to the PlotView.
        '''

        plot_pres = PlotPresenter(self.mock_plot_view)
        plot_pres.register_master(self.mock_main_presenter)
        plot_pres.set_dict(self.fake_dict)

        self.mock_plot_view.reset_mock()
        self.mock_main_presenter.reset_mock()

        '''
        Create fake parameters that correspond with a request to generate a 1D plot from the "threedims" dataset using
        'x' as the x-axis, 'y' as the y-axis, and a slider/stepper value of 4 for the remaining dimension.
        '''
        fake_key = "threedims"
        fake_x = 'x'
        fake_y = 'y'
        fake_slice = {'z': 4}

        plot_pres.create_twodim_plot(fake_key, fake_x, fake_y, fake_slice)

        # Generate the expected sliced array from these parameters
        arr = self.fake_dict[fake_key].data.isel(fake_slice).transpose(fake_y, fake_x)

        '''
        Check for equality between the array that has just been created and the argument sent to the PlotView. This is
        done using xarray's built in equality function.
        '''
        self.assertTrue(arr.equals(self.mock_plot_view.plot_image.call_args[0][0]))

        # Check that the x and y axes labels have been changed, and that the relevant Plot elements have been updated
        self.mock_plot_view.label_x_axis.assert_called_once_with(fake_x)
        self.mock_plot_view.label_y_axis.assert_called_once_with(fake_y)
        self.mock_plot_view.draw_plot.assert_called_once()
        self.mock_main_presenter.update_toolbar.assert_called_once()
