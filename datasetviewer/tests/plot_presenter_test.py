import unittest
import mock

import xarray as xr
import numpy as np

from datasetviewer.mainview.interfaces.MainViewInterface import MainViewInterface
from datasetviewer.plot.PlotView import PlotView
from datasetviewer.plot.PlotPresenter import PlotPresenter

class PlotPresenterTest(unittest.TestCase):

    def setUp(self):

        self.mock_main_view = mock.create_autospec(MainViewInterface)
        self.mock_plot_view = mock.create_autospec(PlotView)


        self.fake_data = xr.Dataset({'good': (['x', 'y', 'z'], np.random.rand(3, 4, 5)),
                                     'valid': (['b'], np.random.rand(3)),
                                     'alsogood': (['c', 'd', 'e', 'f'], np.random.rand(3, 4, 5, 6))})

    def test_clear_plot(self):
        '''
        Test that loading a data array causes the plot to be cleared.
        '''

        plot_pres = PlotPresenter(self.mock_plot_view)
        plot_pres.clear_plot = mock.MagicMock()
        plot_pres.create_default_plot(self.fake_data.alsogood)
        plot_pres.clear_plot.assert_called_once()

    def test_dim_call(self):

        plot_pres = PlotPresenter(self.mock_plot_view)

        plot_pres.create_onedim_plot = mock.MagicMock()
        plot_pres.create_twodim_plot = mock.MagicMock()

        plot_pres.create_default_plot(self.fake_data.valid)
        plot_pres.create_onedim_plot.assert_called_once()

        plot_pres.create_default_plot(self.fake_data.alsogood)
        plot_pres.create_twodim_plot.assert_called_once()
