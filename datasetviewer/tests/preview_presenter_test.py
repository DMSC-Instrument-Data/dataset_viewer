import unittest
import mock
from mock import MagicMock, patch, Mock, PropertyMock

from collections import OrderedDict as DataSet

from enum import Enum

from datasetviewer.preview.PreviewPresenter import PreviewPresenter
from datasetviewer.preview.PreviewView import PreviewView
from datasetviewer.preview.Command import Command
from datasetviewer.dataset.DataSetSource import DataSetSource


class PreviewPresenterTest(unittest.TestCase):

    def setUp(self):

        self.view = mock.create_autospec(PreviewView)
        self.source = mock.create_autospec(DataSetSource)

        mock_var_name = "Key"
        mock_var_dims = (8, 5)

        self.fake_data = Mock(dimension_size=mock_var_dims)
        type(self.fake_data).name = PropertyMock(return_value=mock_var_name)
        self.fake_preview_text = mock_var_name + "\n" + str(mock_var_dims)

        fake_dict = DataSet()
        fake_dict[self.fake_data.name] = self.fake_data
        self.source.get_element = MagicMock(side_effect=lambda key: fake_dict[key])
        self.source.get_data = MagicMock(return_value=fake_dict)

    def test_presenter_throws_if_view_none(self):

        with self.assertRaises(ValueError):
            PreviewPresenter(view=None, source=self.source)

    def test_presenter_throws_if_source_none(self):

        with self.assertRaises(ValueError):
            PreviewPresenter(view=self.view, source=None)

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

    def test_notify_throws_exceptions(self):

        prev_presenter = PreviewPresenter(view=self.view, source=self.source)

        # noinspection PyArgumentList
        fake_enum = Enum(value='invalid', names=[('bad_command', -200000)])

        with self.assertRaises(ValueError):
            prev_presenter.notify(fake_enum.bad_command)

    def test_notify_doesnt_throw_exception(self):

        prev_presenter = PreviewPresenter(view=self.view, source=self.source)

        for command in Command:

            try:
                prev_presenter.notify(command)

            except ValueError:
                self.fail("Command " + command + " raised an Exception.")
