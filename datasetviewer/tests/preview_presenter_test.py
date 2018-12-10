import unittest
import mock

from datasetviewer.preview.PreviewPresenter import PreviewPresenter
from datasetviewer.preview.PreviewView import PreviewView
from datasetviewer.source.DataSetSource import DataSetSource


class PreviewPresenterTest(unittest.TestCase):

    def setUp(self):
        self.view = mock.create_autospec(PreviewView)
        self.source = mock.create_autospec(DataSetSource)

    def test_presenter_throws_if_view_none(self):
        with self.assertRaises(ValueError):
            prev_presenter = PreviewPresenter(view=None, source=self.source)

    def test_presenter_throws_if_source_none(self):
        with self.assertRaises(ValueError):
            prev_presenter = PreviewPresenter(view=self.view, source=None)
