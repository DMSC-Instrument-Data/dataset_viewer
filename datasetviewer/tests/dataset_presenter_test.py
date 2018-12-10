import unittest
import mock

from datasetviewer.preview import PreviewPresenter
from datasetviewer.preview import PreviewView
from datasetviewer.preview import PreviewSource

class PreviewPresenterTest(unittest.TestCase):

    def setUp():
        self.view = mock.create_autospec(PreviewView)
        self.source = mock.create_autospec(PreviewSource)

    def test_presenter_throws_if_view_none(self):
        with self.assertRaises(ValueError):
            p = PreviewPresenter(view=None, source=self.source)

    def test_presenter_throws_if_source_none(self):
        with self.assertRaises(ValueError):
            p = PreviewPresenter(view=self.view, source=None)

