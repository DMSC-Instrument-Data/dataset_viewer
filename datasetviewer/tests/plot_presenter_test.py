import unittest
import mock

import xarray as xr

from datasetviewer.mainview.interfaces.MainViewInterface import MainViewInterface
from datasetviewer.plot.PlotView import PlotView
from datasetviewer.plot.PlotPresenter import PlotPresenter

class PlotPresenterTest(unittest.TestCase):

    def setUp(self):

        self.mock_main_view = mock.create_autospec(MainViewInterface)
        self.mock_plot_view = mock.create_autospec(PlotView)


        self.onedim_data = xr.Dataset()
        self.twodim_data = xr.Dataset()

    def test_clear_plot(self):
        '''
        Test that loading a data array causes the plot to be cleared.
        '''

        plot_pres = PlotPresenter(self.mock_plot_view)

        plot_pres.clear_plot = mock.MagicMock()

        plot_pres.create_default_plot(self.onedim_data)

        plot_pres.clear_plot.assert_called_once()

