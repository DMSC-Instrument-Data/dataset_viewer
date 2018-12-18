import unittest

import mock

import xarray as xr

from datasetviewer.mainview.interfaces.MainView import MainView
from datasetviewer.mainview.MainViewPresenter import MainViewPresenter
from datasetviewer.preview.PreviewPresenter import PreviewPresenter
from datasetviewer.presenter.SubPresenter import SubPresenter


class MainViewPresenterTest(unittest.TestCase):

    def setUp(self):

        self.main_view = mock.create_autospec(MainView)
        self.source = mock.Mock()
        self.sub_presenters = [mock.create_autospec(SubPresenter) for _ in range(10)]
        self.preview_presenter = PreviewPresenter(mock.Mock())
        self.preview_presenter.set_data = mock.MagicMock()
        self.fake_data = xr.Dataset().variables

    def test_presenter_throws_if_view_none(self):

        with self.assertRaises(ValueError):
            MainViewPresenter(None, *self.sub_presenters)

    def test_main_throws_if_sub_none(self):

        badsubpresenters = self.sub_presenters + [None]

        with self.assertRaises(ValueError):
            MainViewPresenter(self.main_view, *badsubpresenters)

    def test_constructor_success(self):

        main_view_presenter = MainViewPresenter(self.main_view, *self.sub_presenters)

        for presenter in self.sub_presenters:
            presenter.register_master.assert_called_once_with(main_view_presenter)

    def test_set_data_to_preview_presenter(self):

        sub_presenters = self.sub_presenters + [self.preview_presenter]
        main_view_presenter = MainViewPresenter(self.main_view, *sub_presenters)

        main_view_presenter.set_data(self.fake_data)
        self.preview_presenter.set_data.assert_called_once_with(self.fake_data)
