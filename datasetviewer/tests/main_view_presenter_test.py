import unittest
import mock
from mock import MagicMock, patch, Mock

from datasetviewer.mainview.MainView import MainView
from datasetviewer.mainview.MainViewPresenter import MainViewPresenter
from datasetviewer.preview.Command import Command as PreviewCommand
from datasetviewer.datasource.Command import Command as DataCommand

class MainViewPresenterTest(unittest.TestCase):

    def setUp(self):

        self.mainview = mock.create_autospec(MainView)

    def test_constructor_sucess(self):

        subpresenters = [Mock() for i in range(10)]
        main_view_presenter = MainViewPresenter(self.mainview, *subpresenters)
        for presenter in subpresenters:
            presenter.register_master.assert_called_once_with(main_view_presenter)

    def test_notify_throws_exception(self):

        subpresenters = [Mock() for i in range(10)]
        main_view_presenter = MainViewPresenter(self.mainview, *subpresenters)

        with self.assertRaises(ValueError):
            main_view_presenter.notify("BADCOMMAND")

    def test_notify_doesnt_throw_exception(self):

        subpresenters = [Mock() for i in range(10)]
        main_view_presenter = MainViewPresenter(self.mainview, *subpresenters)

        valid_commands = [c for c in PreviewCommand] + [c for c in DataCommand]

        try:
            for c in valid_commands:
                main_view_presenter.notify(c)
        except ValueError:
            self.fail("Exception thrown my MainViewPresenter.notify for command: " + c)
