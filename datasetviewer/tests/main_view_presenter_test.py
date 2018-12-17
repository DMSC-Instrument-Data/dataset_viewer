import unittest
from enum import Enum

import mock

from datasetviewer.mainview.interfaces.MainView import MainView
from datasetviewer.mainview.MainViewPresenter import MainViewPresenter
from datasetviewer.preview.Command import Command as PreviewCommand
from datasetviewer.preview.PreviewPresenter import PreviewPresenter
from datasetviewer.presenter.SubPresenter import SubPresenter
from datasetviewer.fileloader.Command import Command as FileCommand


class MainViewPresenterTest(unittest.TestCase):

    def setUp(self):

        self.main_view = mock.create_autospec(MainView)
        self.sub_presenters = [mock.create_autospec(SubPresenter) for _ in range(10)]
        self.preview_presenter = PreviewPresenter(mock.Mock(), mock.Mock())
        self.preview_presenter.populate_preview_list = mock.MagicMock()

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

    def test_notify_throws_exception(self):

        main_view_presenter = MainViewPresenter(self.main_view, *self.sub_presenters)

        # noinspection PyArgumentList
        fake_enum = Enum(value='invalid', names=[('bad_command', -200000)])

        with self.assertRaises(ValueError):
            main_view_presenter.notify(fake_enum.bad_command)

    def test_notify_doesnt_throw_exception(self):

        subpresenters = self.sub_presenters + [self.preview_presenter]
        main_view_presenter = MainViewPresenter(self.main_view, *subpresenters)
        valid_commands = [c for c in PreviewCommand] + [FileCommand.FILEREADSUCCESS]

        for command in valid_commands:
            try:
                main_view_presenter.notify(command)
            except ValueError:
                self.fail("Exception thrown by MainViewPresenter.notify for command: " + str(command))

    def test_file_read_generates_preview(self):

        subpresenters = self.sub_presenters + [self.preview_presenter]
        main_view_presenter = MainViewPresenter(self.main_view, *subpresenters)
        main_view_presenter.notify(FileCommand.FILEREADSUCCESS)
        subpresenters[-1].populate_preview_list.assert_called_once()
