import unittest

import mock
from mock import MagicMock, patch, Mock, PropertyMock

from datasetviewer.fileloader.FileReader import FileReader
from datasetviewer.fileloader.FileLoaderPresenter import FileLoaderPresenter
from datasetviewer.mainview.MainViewPresenter import MainViewPresenter


class FileLoaderPresenterTest(unittest.TestCase):

    def setUp(self):
        self.main_presenter = mock.create_autospec(MainViewPresenter)

    def test_file_to_model(self):
        # Test that the presenter correctly loads a file and passes this data to the model
        pass

    def test_register_main_presenter(self):

        fl_presenter = FileLoaderPresenter(None, None)
        fl_presenter.register_master(self.main_presenter)

        self.main_presenter.subscribe_subpresenter.assert_called_once_with(fl_presenter)
