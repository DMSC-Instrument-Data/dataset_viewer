import unittest
import mock
from mock import MagicMock, patch

from collections import OrderedDict as DataSet

from datasetviewer.preview.PreviewPresenter import PreviewPresenter
from datasetviewer.preview.PreviewView import PreviewView
from datasetviewer.preview.Command import Command
from datasetviewer.source.DataSetSource import DataSetSource
from datasetviewer.source.Variable import Variable



class PreviewPresenterTest(unittest.TestCase):

    def setUp(self):

        self.view = mock.create_autospec(PreviewView)
        self.source = mock.create_autospec(DataSetSource)

        self.fake_data = Variable()
        self.fake_data.name = "Key"
        self.fake_data.dimension_size = (8,5)
        self.fake_preview_text = self.fake_data.name + "\n" + str(self.fake_data.dimension_size)

        fake_dict = DataSet()
        fake_dict[self.fake_data.name] = self.fake_data
        self.source.get_element = MagicMock(side_effect=lambda key: fake_dict[key])
        self.source.get_data = MagicMock(return_value=fake_dict)

    def test_presenter_throws_if_view_none(self):

        with self.assertRaises(ValueError):
            prev_presenter = PreviewPresenter(view=None, source=self.source)

    def test_presenter_throws_if_source_none(self):

        with self.assertRaises(ValueError):
            prev_presenter = PreviewPresenter(view=self.view, source=None)

    def test_create_preview_text(self):

        prev_presenter = PreviewPresenter(view=self.view, source=self.source)

        self.assertEqual(prev_presenter.create_preview_text(self.fake_data.name), self.fake_preview_text)

    def test_call_to_create_preview_text(self):
        
        prev_presenter = PreviewPresenter(view=self.view, source=self.source)

        with patch('datasetviewer.preview.PreviewPresenter.PreviewPresenter.create_preview_text') as prev_text:
            prev_presenter.add_preview_entry(self.fake_data.name)
            prev_text.assert_called_once()

    def test_create_preview_calls_add_to_list(self):

        prev_presenter = PreviewPresenter(view=self.view, source=self.source)
        prev_presenter.add_preview_entry(self.fake_data.name)
        self.view.add_entry_to_list.assert_called_once_with(self.fake_preview_text)

    def test_populate_preview_list(self):

        prev_presenter = PreviewPresenter(view=self.view, source=self.source)
        prev_presenter.populate_preview_list()

        self.source.get_data.assert_called_once()

    def test_call_to_add_preview_entry(self):

        prev_presenter = PreviewPresenter(view=self.view, source=self.source)

        with patch('datasetviewer.preview.PreviewPresenter.PreviewPresenter.add_preview_entry') as add_prev:
            prev_presenter.populate_preview_list()
            add_prev.assert_called_once_with(self.fake_data.name)

    def test_notify_exceptions(self):

        prev_presenter = PreviewPresenter(view=self.view, source=self.source)

        with self.assertRaises(ValueError):
            prev_presenter.notify("BADCOMMAND")

        # Have to add to this list as Command class is expanded
        good_commands = [Command.Selection]

        try:
            for command in good_commands:
                prev_presenter.notify(command)
                
        except ValueError:
            self.fail("Command " + command + " raised an Exception.")