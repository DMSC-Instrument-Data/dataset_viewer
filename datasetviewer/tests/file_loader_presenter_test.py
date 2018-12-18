import unittest

import mock

from enum import Enum

from datasetviewer.fileloader.FileLoaderPresenter import FileLoaderPresenter
from datasetviewer.fileloader.interfaces.FileLoaderView import FileLoaderView
from datasetviewer.fileloader.Command import Command
from datasetviewer.mainview.MainViewPresenter import MainViewPresenter

import xarray as xr

class FileLoaderPresenterTest(unittest.TestCase):

    def setUp(self):

        self.main_presenter = mock.create_autospec(MainViewPresenter)
        self.main_presenter.set_data = mock.MagicMock()
        self.view = mock.create_autospec(FileLoaderView)

        self.dummy_data = xr.Dataset()
        self.fake_file_path = "filepath"

        self.view.get_selected_file_path = mock.MagicMock(side_effect=lambda: self.fake_file_path)

        self.fl_presenter = FileLoaderPresenter(self.view)
        self.fl_presenter.register_master(self.main_presenter)

    def test_presenter_throws_if_view_none(self):

        with self.assertRaises(ValueError):
            FileLoaderPresenter(None)

    def test_register_master(self):

        fl_presenter = FileLoaderPresenter(self.view)

        main_presenter = mock.create_autospec(MainViewPresenter)
        fl_presenter.register_master(main_presenter)

        main_presenter.subscribe_subpresenter.assert_called_once_with(fl_presenter)

    def test_file_selection_calls_get_path(self):

        fl_presenter = FileLoaderPresenter(self.view)
        fl_presenter.register_master(self.main_presenter)
        fl_presenter.load_data = mock.MagicMock()
        fl_presenter.notify(Command.FILEOPENREQUEST)
        self.view.get_selected_file_path.assert_called_once()

    def test_bad_file_shows_message(self):

        with mock.patch("datasetviewer.fileloader.FileLoaderTool.open_dataset",
                        side_effect=lambda path: self.dummy_data):

            self.fl_presenter.load_data(self.fake_file_path)
            self.view.show_reject_file_message.assert_called_once()

    def test_load_file(self):

        fl_presenter = FileLoaderPresenter(self.view)
        fl_presenter.register_master(self.main_presenter)
        fl_presenter.load_data = mock.MagicMock(side_effect = lambda path: self.dummy_data.variables)

        fl_presenter.notify(Command.FILEOPENREQUEST)
        fl_presenter.load_data.assert_called_once_with(self.fake_file_path)

    def test_file_open_success_informs_main_presenter(self):

        with mock.patch("datasetviewer.fileloader.FileLoaderTool.FileLoaderTool.file_to_dict",
                        side_effect = lambda path: self.dummy_data.variables):

            self.fl_presenter.notify(Command.FILEOPENREQUEST)
            self.main_presenter.set_data.assert_called_once_with(self.dummy_data.variables)

    def test_unknown_command_raises(self):

        fl_presenter = FileLoaderPresenter(self.view)

        fake_enum = Enum(value='invalid', names=[('bad_command', -200000)])

        with self.assertRaises(ValueError):
            fl_presenter.notify(fake_enum.bad_command)
