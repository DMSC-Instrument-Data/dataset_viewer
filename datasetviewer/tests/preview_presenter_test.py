import unittest
import mock

import numpy as np

from collections import OrderedDict as DataSet

from datasetviewer.preview.PreviewPresenter import PreviewPresenter
from datasetviewer.preview.interfaces.PreviewView import PreviewView
from datasetviewer.mainview.MainViewPresenter import MainViewPresenter
from datasetviewer.dataset.Variable import Variable


class PreviewPresenterTest(unittest.TestCase):

    def setUp(self):

        self.view = mock.create_autospec(PreviewView)

        self.master = mock.create_autospec(MainViewPresenter)

        self.var_name = "Key"
        self.var_dims = (8, 5)
        self.fake_data = DataSet()
        self.fake_data[self.var_name] = Variable(self.var_name, np.random.rand(*self.var_dims))

        self.fake_preview_text = self.var_name + "\n" + str(self.var_dims)

    def test_presenter_throws_if_view_none(self):

        with self.assertRaises(ValueError):
            PreviewPresenter(None)

    def test_create_preview_text(self):

        prev_presenter = PreviewPresenter(self.view)
        prev_presenter.set_data(self.fake_data)
        self.assertEqual(prev_presenter.create_preview_text(self.var_name), self.fake_preview_text)

    def test_call_to_create_preview_text(self):

        prev_presenter = PreviewPresenter(self.view)

        with mock.patch('datasetviewer.preview.PreviewPresenter.PreviewPresenter.create_preview_text') as prev_text:
            prev_presenter.add_preview_entry(self.var_name)
            prev_text.assert_called_once()

    def test_create_preview_calls_add_to_list(self):

        prev_presenter = PreviewPresenter(self.view)
        prev_presenter.set_data(self.fake_data)
        self.view.add_entry_to_list.assert_called_once_with(self.fake_preview_text)

    def test_call_to_add_preview_entry(self):

        prev_presenter = PreviewPresenter(self.view)
        prev_presenter.set_data(self.fake_data)

        with mock.patch('datasetviewer.preview.PreviewPresenter.PreviewPresenter.add_preview_entry') as add_prev:
            prev_presenter.populate_preview_list()
            add_prev.assert_called_once_with(self.var_name)

    def test_register_master(self):

        prev_presenter = PreviewPresenter(self.view)
        prev_presenter.register_master(self.master)
        self.master.subscribe_preview_presenter.assert_called_once_with(prev_presenter)
