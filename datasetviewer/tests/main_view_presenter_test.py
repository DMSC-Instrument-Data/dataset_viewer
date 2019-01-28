import unittest

import mock

import xarray as xr

from datasetviewer.mainview.MainViewPresenter import MainViewPresenter
from datasetviewer.mainview.interfaces.MainViewInterface import MainViewInterface
from datasetviewer.preview.interfaces.PreviewPresenterInterface import PreviewPresenterInterface
from datasetviewer.plot.interfaces.PlotPresenterInterface import PlotPresenterInterface
from datasetviewer.fileloader.interfaces.FileLoaderPresenterInterface import FileLoaderPresenterInterface
from datasetviewer.stack.interfaces.StackPresenterInterface import StackPresenterInterface
from datasetviewer.dataset.Variable import Variable

from collections import OrderedDict as DataSet
import numpy as np

class MainViewPresenterTest(unittest.TestCase):

    def setUp(self):

        self.mock_main_view = mock.create_autospec(MainViewInterface)

        # Mock the SubPresenters
        self.mock_preview_presenter = mock.create_autospec(PreviewPresenterInterface)
        self.mock_plot_presenter = mock.create_autospec(PlotPresenterInterface)
        self.mock_file_loader_presenter = mock.create_autospec(FileLoaderPresenterInterface)
        self.mock_stack_presenter = mock.create_autospec(StackPresenterInterface)

        self.mock_sub_presenters = [self.mock_preview_presenter,
                                    self.mock_plot_presenter,
                                    self.mock_file_loader_presenter,
                                    self.mock_stack_presenter]

        # Create a fake data dictionary
        self.fake_dict = DataSet()
        self.fake_dict["good"] = Variable("good", xr.DataArray(np.random.rand(3, 4, 5), dims=['x', 'y', 'z']))
        self.fake_dict["valid"] = Variable("valid", xr.DataArray(np.random.rand(3), dims=['b']))

    def test_presenter_throws_if_view_none(self):
        '''
        Test that the MainViewPresenter throws an Exception if the MainView is None.
        '''
        with self.assertRaises(ValueError):
            MainViewPresenter(None, *self.mock_sub_presenters)

    def test_constructor_throws_if_subpresenter_none(self):
        '''
        Test that the MainViewPresenter throws an Exception if any of the SubPresenters are None.
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

    def test_set_dict(self):
        '''
        Test that the MainViewPresenter passes a data dictionary to the PreviewPresenter, PlotPresenter, and
        StackPresenter when its data attribute is set.
        '''

        main_view_presenter = MainViewPresenter(self.mock_main_view, *self.mock_sub_presenters)
        main_view_presenter.subscribe_preview_presenter(self.mock_preview_presenter)
        main_view_presenter.subscribe_plot_presenter(self.mock_plot_presenter)
        main_view_presenter.subscribe_stack_presenter(self.mock_stack_presenter)

        main_view_presenter.set_dict(self.fake_dict)
        self.mock_preview_presenter.set_dict.assert_called_once_with(self.fake_dict)
        self.mock_plot_presenter.set_dict.assert_called_once_with(self.fake_dict)
        self.mock_stack_presenter.set_dict.assert_called_once_with(self.fake_dict)

    def test_create_default_plot(self):
        '''
        Test that a call to the MainViewPresenter `create_default_plot` function calls another function of the same
        name in the PlotPresenter
        '''

        main_view_presenter = MainViewPresenter(self.mock_main_view, *self.mock_sub_presenters)
        main_view_presenter.subscribe_plot_presenter(self.mock_plot_presenter)
        main_view_presenter.subscribe_preview_presenter(self.mock_preview_presenter)
        main_view_presenter.subscribe_stack_presenter(self.mock_stack_presenter)
        main_view_presenter.set_dict(self.fake_dict)

        # Instruct the MainViewPresenter to generate the default plot from one of the elements in the data dictionary
        main_view_presenter.change_current_key("good")

        # Test that the `create_default_plot` method in the PlotPresenter is called with the same key.
        self.mock_plot_presenter.create_default_plot.assert_called_once_with("good")
        self.mock_stack_presenter.change_stack_face.assert_called_once_with("good")

    def test_update_toolbar(self):
        '''
        Test that the `update_toolbar` method in the MainViewPresenter calls another function of the same name in the
        MainView.
        '''

        main_view_presenter = MainViewPresenter(self.mock_main_view, *self.mock_sub_presenters)
        main_view_presenter.update_toolbar()
        self.mock_main_view.update_toolbar.assert_called_once()

    def test_create_onedim_plot(self):

        main_view_presenter = MainViewPresenter(self.mock_main_view, *self.mock_sub_presenters)
        main_view_presenter.subscribe_plot_presenter(self.mock_plot_presenter)

        main_view_presenter.create_onedim_plot("fakekey",'xdim',{})

        self.mock_plot_presenter.create_onedim_plot.assert_called_once_with("fakekey", 'xdim', {})

    def test_create_twodim_plot(self):

        main_view_presenter = MainViewPresenter(self.mock_main_view, *self.mock_sub_presenters)
        main_view_presenter.subscribe_plot_presenter(self.mock_plot_presenter)

        main_view_presenter.create_twodim_plot("fakekey",'xdim', 'ydim', {})

        self.mock_plot_presenter.create_twodim_plot.assert_called_once_with("fakekey", 'xdim', 'ydim', {})
