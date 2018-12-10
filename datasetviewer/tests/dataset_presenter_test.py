import unittest
import mock

from datasetviewer.preview import PreviewPresenter
from datasetviewer.preview import PreviewView
from datasetviewer.preview import PreviewSource

class PreviewPresenterTest(unittest.TestCase):

    def setUp():
        self.view = mock.create_autospec(PreviewView)
        self.source = mock.create_autospec(PreviewSource)


