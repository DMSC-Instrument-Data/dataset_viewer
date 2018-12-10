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

        # Create a Variable for the Source Mock
        fake_data = Variable()
        fake_name = "Key"
        fake_dim_size = (8, 5)
        fake_data.name = fake_name
        fake_data.dimension_size = fake_dim_size

        # Instruct the Source to return the fake Variable when given its matching Key 
        self.source.get_element = MagicMock(side_effect=lambda key: fake_data)

        # Create a Presenter with the Source mock
        prev_presenter = PreviewPresenter(view=self.view, source=self.source)

        expected_text = fake_name + "\n" + str(fake_dim_size)
        self.assertEqual(prev_presenter.create_preview_text(fake_name), expected_text)
