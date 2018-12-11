import unittest
import mock
from mock import MagicMock, patch, Mock

from datasetviewer.mainview.MainView import MainView
from datasetviewer.mainview.MainViewPresenter import MainViewPresenter


class MainViewPresenterTest(unittest.TestCase):

    def setUp(self):

        self.mainview = mock.create_autospec(MainView)

    def test_constructor_sucess(self):

        subpresenters = [Mock() for i in range(10)]
        main_view_presenter = MainViewPresenter(self.mainview, *subpresenters)
        for presenter in subpresenters:
            presenter.register_master.assert_called_once_with(main_view_presenter)
