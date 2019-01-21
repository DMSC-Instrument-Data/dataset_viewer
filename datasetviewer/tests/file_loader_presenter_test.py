import unittest

import mock

from enum import Enum

from datasetviewer.fileloader.FileLoaderPresenter import FileLoaderPresenter
from datasetviewer.fileloader.interfaces.FileLoaderViewInterface import FileLoaderViewInterface
from datasetviewer.mainview.interfaces.MainViewPresenterInterface import MainViewPresenterInterface
from datasetviewer.fileloader.Command import Command

import xarray as xr

class FileLoaderPresenterTest(unittest.TestCase):

    def setUp(self):

        # Create a mock of the MainViewPresenter
        self.mock_main_presenter = mock.create_autospec(MainViewPresenterInterface)
        self.mock_main_presenter.set_dict = mock.MagicMock()

        # Create a mock of the FileLoaderView
        self.mock_view = mock.create_autospec(FileLoaderViewInterface)

        # Create fake empty data, a fake file path, and a mock that returns a fake file path
        self.empty_data = xr.Dataset()
        self.fake_file_path = ("filepath", ".ext")
        self.mock_view.get_selected_file_path = mock.MagicMock(side_effect=lambda: self.fake_file_path)

    def test_presenter_throws_if_view_none(self):
        '''
        Test that the FileLoaderPresenter throws an Exception when the FileLoaderView is None.
        '''
        with self.assertRaises(ValueError):
            FileLoaderPresenter(None)

    def test_file_selection_calls_get_path_on_view(self):
        '''
        Test that a FILEOPENREQUEST in the FileLoaderPresenter's `notify` function causes the `get_selected_file_path`
        method on the FileLoaderVIew to be called.
        '''
        fl_presenter = FileLoaderPresenter(self.mock_view)
        fl_presenter.register_master(self.mock_main_presenter)

        # Mock the `_load_data` method so that no actual file-reading occurs
        fl_presenter._load_data = mock.MagicMock()

        # Notify the FileLoaderPresenter of a FILE
        fl_presenter.notify(Command.FILEOPENREQUEST)
        self.mock_view.get_selected_file_path.assert_called_once()

    def test_bad_file_shows_message_on_view(self):
        '''
        Test that the request to open a bad file causes the view to display a message.
        '''

        fl_presenter = FileLoaderPresenter(self.mock_view)
        fl_presenter.register_master(self.mock_main_presenter)

        # Mock the `open_dataset` function in the FileLoaderTool so that it returns a bad dataset
        with mock.patch("datasetviewer.fileloader.FileLoaderTool.open_dataset",
                        side_effect=lambda path: self.empty_data):

            fl_presenter.notify(Command.FILEOPENREQUEST)

            # Check that loading a bad dataset caused a message to be displayed on the view indicating that the file
            # was rejected

            self.mock_view.show_reject_file_message.assert_called_once()

            # Check that the `set_dict` method in the MainPresenter was not called as a result of the file being
            # rejected
            self.mock_main_presenter.set_dict.assert_not_called()

    def test_closing_filedialog_does_nothing(self):
        '''
        Test that closing the FileDialog without choosing a file causes the presenter to return without attempting
        to open or interpret a file
        '''

        mock_view = mock.create_autospec(FileLoaderViewInterface)

        # Tell the mock to behave as if the FileDialog was closed without a file being chosen
        mock_view.get_selected_file_path = mock.MagicMock(side_effect = lambda: ('',''))

        fl_presenter = FileLoaderPresenter(mock_view)
        fl_presenter.register_master(self.mock_main_presenter)
        fl_presenter._load_data = mock.MagicMock()

        fl_presenter.notify(Command.FILEOPENREQUEST)
        fl_presenter._load_data.assert_not_called()
        self.mock_main_presenter.set_dict.assert_not_called()

    def test_load_file(self):
        '''
        Test that a FILEOPENREQUEST in `notify` causes the `_load_data` method to be called with the expected argument.
        '''
        fl_presenter = FileLoaderPresenter(self.mock_view)
        fl_presenter.register_master(self.mock_main_presenter)
        fl_presenter._load_data = mock.MagicMock(side_effect = lambda path: self.empty_data.variables)

        fl_presenter.notify(Command.FILEOPENREQUEST)
        fl_presenter._load_data.assert_called_once_with(self.fake_file_path[0])

    def test_file_open_success_informs_main_presenter(self):
        '''
        Test that successfully opening a file in the FileLoaderPresenter causes the resulting DataSet to be sent to the
        MainViewPresenter.
        '''

        fl_presenter = FileLoaderPresenter(self.mock_view)
        fl_presenter.register_master(self.mock_main_presenter)

        with mock.patch("datasetviewer.fileloader.FileLoaderTool.file_to_dict",
                        side_effect = lambda path: self.empty_data.variables):

            fl_presenter.notify(Command.FILEOPENREQUEST)
            self.mock_main_presenter.set_dict.assert_called_once_with(self.empty_data.variables)

    def test_notify_raises_if_command_unknown(self):
        '''
        Test that an exception is thrown if notify is called with a command it does not recognise.
        '''
        fl_presenter = FileLoaderPresenter(self.mock_view)

        fake_enum = Enum(value='invalid', names=[('bad_command', -200000)])

        with self.assertRaises(ValueError):
            fl_presenter.notify(fake_enum.bad_command)
