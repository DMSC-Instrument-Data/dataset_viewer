import unittest

import mock

import xarray as xr

from datasetviewer.mainview.MainViewPresenter import MainViewPresenter
from datasetviewer.mainview.interfaces.MainViewInterface import MainViewInterface
from datasetviewer.preview.interfaces.PreviewPresenterInterface import PreviewPresenterInterface
from datasetviewer.subpresenter.SubPresenterInterface import SubPresenterInterface
from datasetviewer.plot.interfaces.PlotPresenterInterface import PlotPresenterInterface
from datasetviewer.dataset.Variable import Variable

from collections import OrderedDict as DataSet

class MainViewPresenterTest(unittest.TestCase):

    def setUp(self):

        self.mock_main_view = mock.create_autospec(MainViewInterface)
        self.mock_source = mock.Mock()
        self.mock_sub_presenters = [mock.create_autospec(SubPresenterInterface) for _ in range(10)]
        self.mock_preview_presenter = mock.create_autospec(PreviewPresenterInterface)
        self.mock_plot_presenter = mock.create_autospec(PlotPresenterInterface)
        self.fake_data = xr.Dataset().variables

    def test_presenter_throws_if_view_none(self):
        '''
        Test that the MainViewPresenter throws an Exception if the MainView is None.
        '''
        with self.assertRaises(ValueError):
            MainViewPresenter(None, *self.mock_sub_presenters)

    def test_constructor_throws_if_subpresenter_none(self):
        '''
        Test that the MainViewPresenter throws an Exception if any of the SubPresenters are None.
        :return:
        '''
        badsubpresenters = self.mock_sub_presenters + [None]

        with self.assertRaises(ValueError):
            MainViewPresenter(self.mock_main_view, *badsubpresenters)

    def test_constructor_success(self):
        '''
        Test that the `register_master` method is called in each of the SubPresenters when the MainViewPresenter is
        initialised.
        '''
        main_view_presenter = MainViewPresenter(self.mock_main_view, *self.mock_sub_presenters)

        for presenter in self.mock_sub_presenters:
            presenter.register_master.assert_called_once_with(main_view_presenter)

    def test_set_data_to_preview_presenter(self):
        '''
        Test that the MainViewPresenter passes a data dictionary to the PreviewPresenter when its data attribute is set
        to a value.
        '''
        sub_presenters = self.mock_sub_presenters + [self.mock_preview_presenter]
        main_view_presenter = MainViewPresenter(self.mock_main_view, *sub_presenters)
        main_view_presenter.subscribe_preview_presenter(self.mock_preview_presenter)

        main_view_presenter.set_data(self.fake_data)
        self.mock_preview_presenter.set_data.assert_called_once_with(self.fake_data)

    def test_create_default_plot(self):
        '''
        Test that a call to the MainViewPresenter `create_default_plot` function calls another function of the same
        name in the PlotPresenter
        '''
        sub_presenters = self.mock_sub_presenters + [self.mock_plot_presenter]
        main_view_presenter = MainViewPresenter(self.mock_main_view, *sub_presenters)
        main_view_presenter.subscribe_plot_presenter(self.mock_plot_presenter)

        # Create a fake dataset and place it in the MainViewPresenter
        fake_data = DataSet()
        fake_key = "fake_key"
        fake_elem = Variable(fake_key, self.fake_data)
        fake_data["fake_key"] = fake_elem
        main_view_presenter._data = fake_data

        main_view_presenter.create_default_plot(fake_key)
        self.mock_plot_presenter.create_default_plot.assert_called_once_with(self.fake_data)
