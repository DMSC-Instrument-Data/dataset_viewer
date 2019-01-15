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

        self.mock_plot_view.ax = mock.PropertyMock()
        self.mock_plot_view.ax.plot = mock.MagicMock()
        self.mock_plot_view.ax.imshow = mock.MagicMock()

        self.fake_data = xr.Dataset({'good': (['x', 'y', 'z'], np.random.rand(3, 4, 5)),
                                     'valid': (['b'], np.random.rand(3)),
                                     'twodims': (['g', 'h'], np.random.rand(3, 8)),
                                     'alsogood': (['c', 'd', 'e', 'f'], np.random.rand(3, 4, 5, 6))})

    def test_clear_plot(self):
        '''
        Test that loading a data array causes the plot to be cleared.
        '''

        plot_pres = PlotPresenter(self.mock_plot_view)
        plot_pres.clear_plot = mock.MagicMock()
        plot_pres.create_default_plot(self.fake_data.alsogood)
        plot_pres.clear_plot.assert_called_once()

    def test_plot_call(self):

        plot_pres = PlotPresenter(self.mock_plot_view)

        plot_pres.create_default_plot(self.fake_data.valid)
        xr.testing.assert_equal(self.mock_plot_view.ax.plot.call_args[0][0], self.fake_data.valid)
