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

    def test_draw_plot(self):
        '''
        Test that the presenter calls the PlotView's draw function after receiving new data.
        '''

        self.mock_plot_view.draw_plot = mock.MagicMock()

        plot_pres = PlotPresenter(self.mock_plot_view)
        plot_pres.register_master(self.mock_main_presenter)
        plot_pres.set_dict(self.fake_dict)

        self.mock_plot_view.draw_plot.assert_called_once()

    def test_new_data_updates_toolbar(self):
        '''
        Test that creating a new plot causes the toolbar to be updated.
        '''

        plot_pres = PlotPresenter(self.mock_plot_view)
        plot_pres.register_master(self.mock_main_presenter)
        plot_pres._dict = self.fake_dict

        plot_pres.create_default_plot("onedim")
        self.mock_main_presenter.update_toolbar.assert_called_once()

    def test_create_onedim_plot(self):

        plot_pres = PlotPresenter(self.mock_plot_view)
        plot_pres.register_master(self.mock_main_presenter)
        plot_pres.set_dict(self.fake_dict)

        fake_key = "threedims"
        fake_x = 'x'
        fake_slice = {'y': 2, 'z': 3}

        plot_pres.create_onedim_plot(fake_key, fake_x, fake_slice)

        arr = self.fake_dict[fake_key].data.isel(fake_slice)

        arr.equals(self.mock_plot_view.plot_line.call_args[0][0])
