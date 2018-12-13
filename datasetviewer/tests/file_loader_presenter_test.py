import unittest

import mock
from mock import patch

from datasetviewer.fileloader.FileLoaderPresenter import FileLoaderPresenter
from datasetviewer.fileloader.interfaces.FileLoaderView import FileLoaderView
from datasetviewer.fileloader.Command import Command
from datasetviewer.dataset.interfaces.DataSetSource import DataSetSource
from datasetviewer.mainview.MainViewPresenter import MainViewPresenter

import xarray as xr

class FileLoaderPresenterTest(unittest.TestCase):

    def setUp(self):

        self.main_presenter = mock.create_autospec(MainViewPresenter)
        self.source = mock.create_autospec(DataSetSource)
        self.view = mock.create_autospec(FileLoaderView)
        self.dummy_data = xr.Dataset()
        self.fake_file_path = "filepath"

        self.fl_presenter = FileLoaderPresenter(self.source, self.view)
        self.fl_presenter.register_master(self.main_presenter)

    def test_register_master(self):

        fl_presenter = FileLoaderPresenter(self.source, self.view)

        main_presenter = mock.create_autospec(MainViewPresenter)
        fl_presenter.register_master(main_presenter)

        main_presenter.subscribe_subpresenter.assert_called_once_with(fl_presenter)

    def test_read_file_to_model(self):

        with patch("datasetviewer.fileloader.FileLoaderTool.FileLoaderTool.file_to_dict",
                   side_effect = lambda path: self.dummy_data.variables) as dummy_file_reader:

            self.fl_presenter.load_data_to_model(self.fake_file_path)
            self.source.set_data.assert_called_once_with(self.dummy_data.variables)

    def test_bad_file_shows_message(self):

        with patch("datasetviewer.fileloader.FileLoaderTool.open_dataset",
                   side_effect = lambda path: self.dummy_data) as dummy_file_reader:

            self.fl_presenter.load_data_to_model(self.fake_file_path)
            self.view.show_reject_file_message.assert_called_once()

    def test_file_open_success_notifies_main_presenter(self):

        with patch("datasetviewer.fileloader.FileLoaderTool.FileLoaderTool.file_to_dict",
                   side_effect = lambda path: self.dummy_data.variables) as dummy_file_reader:

            self.fl_presenter.load_data_to_model(self.fake_file_path)
            self.main_presenter.notify.assert_called_once_with(Command.FILEREADSUCCESS)