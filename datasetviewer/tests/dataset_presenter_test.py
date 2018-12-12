import unittest

import mock
from mock import MagicMock, patch, Mock, PropertyMock

from datasetviewer.dataset.FileReader import FileReader
from datasetviewer.dataset.DataSetPresenter import DataSetPresenter
from datasetviewer.mainview.MainViewPresenter import MainViewPresenter


class DataSetPresenterTest(unittest.TestCase):

    def setUp(self):

        self.main_presenter = mock.create_autospec(MainViewPresenter)

    def test_file_to_model(self):
        pass

    def test_register_main_presenter(self):

        ds_presenter = DataSetPresenter(None, None)
        ds_presenter.register_master(self.main_presenter)

        self.main_presenter.subscribe_subpresenter.assert_called_once_with(ds_presenter)
