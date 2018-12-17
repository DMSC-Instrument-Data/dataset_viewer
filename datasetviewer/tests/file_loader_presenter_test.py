import unittest

import mock

from enum import Enum

from datasetviewer.fileloader.FileLoaderPresenter import FileLoaderPresenter
from datasetviewer.fileloader.interfaces.FileLoaderView import FileLoaderView
from datasetviewer.fileloader.Command import Command
from datasetviewer.dataset.interfaces.DataSetSource import DataSetSource
from datasetviewer.mainview.MainViewPresenter import MainViewPresenter

import xarray as xr

class FileLoaderPresenterTest(unittest.TestCase):

    def setUp(self):

        self.main_presenter = mock.create_autospec(MainViewPresenter)
        self.main_presenter.load_file_to_model = mock.MagicMock()
        self.source = mock.create_autospec(DataSetSource)
        self.view = mock.create_autospec(FileLoaderView)

        self.dummy_data = xr.Dataset()
        self.fake_file_path = "filepath"

        self.view.get_selected_file_path = mock.MagicMock(side_effect=lambda: self.fake_file_path)

        self.fl_presenter = FileLoaderPresenter(self.source, self.view)
        self.fl_presenter.register_master(self.main_presenter)

    def test_presenter_throws_if_source_none(self):

        with self.assertRaises(ValueError):
            FileLoaderPresenter(None, self.view)

    def test_presenter_throws_if_view_none(self):

        with self.assertRaises(ValueError):
            FileLoaderPresenter(self.source, None)

    def test_register_master(self):

        fl_presenter = FileLoaderPresenter(self.source, self.view)

        main_presenter = mock.create_autospec(MainViewPresenter)
        fl_presenter.register_master(main_presenter)

        main_presenter.subscribe_subpresenter.assert_called_once_with(fl_presenter)

    @mock.patch("datasetviewer.fileloader.FileLoaderTool.FileLoaderTool.file_to_dict",
                side_effect=lambda path: xr.Dataset().variables)
    def test_notify_file_selection(self, file_to_dict):

        self.fl_presenter.notify(Command.FILEOPENREQUEST)
        self.view.get_selected_file_path.assert_called_once()

    def test_load_file_in_main_presenter(self):

        self.fl_presenter.notify(Command.FILEOPENREQUEST)
        self.main_presenter.load_file_to_model.assert_called_once_with(self.fake_file_path)

    '''
    @mock.patch("datasetviewer.fileloader.FileLoaderTool.FileLoaderTool.file_to_dict",
                side_effect = lambda path: xr.Dataset().variables)
    def test_file_selection_loads_file(self, file_to_dict):

        self.view.get_selected_file_path = mock.MagicMock(return_value=self.fake_file_path)

        with mock.patch("datasetviewer.fileloader.FileLoaderPresenter.FileLoaderPresenter.load_data_to_model") as load_data:
            self.fl_presenter.notify(Command.FILEOPENREQUEST)
            load_data.assert_called_once()


    def test_read_file_to_model(self):

        with mock.patch("datasetviewer.fileloader.FileLoaderTool.FileLoaderTool.file_to_dict",
                        side_effect = lambda path: self.dummy_data.variables):

            self.fl_presenter.load_data_to_model(self.fake_file_path)
            self.source.set_data.assert_called_once_with(self.dummy_data.variables)

    def test_bad_file_shows_message(self):

        with mock.patch("datasetviewer.fileloader.FileLoaderTool.open_dataset",
                        side_effect = lambda path: self.dummy_data):

            self.fl_presenter.load_data_to_model(self.fake_file_path)
            self.view.show_reject_file_message.assert_called_once()

    def test_file_open_success_informs_main_presenter(self):

        with mock.patch("datasetviewer.fileloader.FileLoaderTool.FileLoaderTool.file_to_dict",
                        side_effect = lambda path: self.dummy_data.variables):

            self.fl_presenter.notify(Command.FILEOPENREQUEST)
            self.main_presenter.create_preview.assert_called_once()
    '''

    def test_unknown_command_raises(self):

        fl_presenter = FileLoaderPresenter(self.source, self.view)

        fake_enum = Enum(value='invalid', names=[('bad_command', -200000)])

        with self.assertRaises(ValueError):
            fl_presenter.notify(fake_enum.bad_command)
