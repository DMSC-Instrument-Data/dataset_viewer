import unittest
import mock
from mock import MagicMock

from collections import OrderedDict as DataSet

from datasetviewer.preview.PreviewPresenter import PreviewPresenter
from datasetviewer.preview.PreviewView import PreviewView
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

    def test_presenter_assignment(self):
        prev_presenter = PreviewPresenter(view=self.view, source=self.source)

        self.assertEqual(prev_presenter._view, self.view)
        self.assertEqual(prev_presenter._source, self.source)

    def test_presenter_throws_if_view_none(self):
        with self.assertRaises(ValueError):
            prev_presenter = PreviewPresenter(view=None, source=self.source)

    def test_presenter_throws_if_source_none(self):
        with self.assertRaises(ValueError):
            prev_presenter = PreviewPresenter(view=self.view, source=None)

    def text_create_preview_calls_get_data(self):
        prev_presenter = PreviewPresenter(view=self.view, source=self.source)

    def test_create_preview_test(self):

        # Create a Presenter with the Source mock
        prev_presenter = PreviewPresenter(view=self.view, source=self.source)

        self.assertEqual(prev_presenter.create_preview_text(self.fake_data.name), self.fake_preview_text)

    def test_add_preview_entry(self):
        
        prev_presenter = PreviewPresenter(view=self.view, source=self.source)
        prev_presenter.add_preview_entry(self.fake_data.name)

        self.view.add_entry_to_list.assert_called_once_with(self.fake_preview_text)

    def test_populate_preview_list(self):

        prev_presenter = PreviewPresenter(view=self.view, source=self.source)
        prev_presenter.populate_preview_list()

        self.source.get_data.assert_called_once()
