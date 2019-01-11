import unittest
import mock

import numpy as np

from collections import OrderedDict as DataSet

from datasetviewer.preview.PreviewPresenter import PreviewPresenter
from datasetviewer.preview.interfaces.PreviewViewInterface import PreviewViewInterface
from datasetviewer.mainview.interfaces.MainViewPresenterInterface import MainViewPresenterInterface
from datasetviewer.preview.Command import Command
from datasetviewer.dataset.Variable import Variable

class PreviewPresenterTest(unittest.TestCase):

    def setUp(self):

        self.mock_preview_view = mock.create_autospec(PreviewViewInterface)

        self.mock_master_presenter = mock.create_autospec(MainViewPresenterInterface)
        self.mock_master_presenter.subscribe_preview_presenter = mock.MagicMock()

        self.var_name = "Key"
        self.var_dims = (8, 5)
        self.fake_data = DataSet()
        self.fake_data[self.var_name] = Variable(self.var_name, np.random.rand(*self.var_dims))

        # The fake preview text that should be generated from the fake data
        self.fake_preview_text = self.var_name + "\n" + str(self.var_dims)

    def test_presenter_throws_if_view_none(self):
        '''
        Ensure that the PreviewPresenter throws an exception when given a None PreviewView.
        '''
        with self.assertRaises(ValueError):
            PreviewPresenter(None)

    def test_create_preview_text(self):
        '''
        Test that the Preview text that is generated after setting the data contains the expected key and data
        dimensions
        '''
        prev_presenter = PreviewPresenter(self.mock_preview_view)
        prev_presenter.set_data(self.fake_data)
        self.assertEqual(prev_presenter._create_preview_text(self.var_name), self.fake_preview_text)

    def test_call_to_create_preview_text(self):
        '''
        Test that the PreviewPresenter calls the `_create_preview_text` method once the `_add_preview_entry` method
        has been called.
        '''
        prev_presenter = PreviewPresenter(self.mock_preview_view)

        with mock.patch('datasetviewer.preview.PreviewPresenter.PreviewPresenter._create_preview_text') as prev_text:
            prev_presenter._add_preview_entry(self.var_name)
            prev_text.assert_called_once()

    def test_create_preview_calls_add_to_list(self):
        '''
        Test that the PreviewPresenter calls the PreviewView's `_add_entry_to_list` method once with the expected text
        once the data attribute has been set in the PreviewPresenter.
        '''
        prev_presenter = PreviewPresenter(self.mock_preview_view)
        prev_presenter.set_data(self.fake_data)
        self.mock_preview_view.add_entry_to_list.assert_called_once_with(self.fake_preview_text)

    def test_register_master(self):
        '''
        Test the two-way link between the PreviewPresenter as its MainViewPresenter master.
        '''
        prev_presenter = PreviewPresenter(self.mock_preview_view)
        prev_presenter.register_master(self.mock_master_presenter)
        self.mock_master_presenter.subscribe_preview_presenter.assert_called_once_with(prev_presenter)

    def test_get_selection(self):
        '''
        Test that the element-selection command causes the presenter to obtain information about the selection from the
        view
        '''

        prev_presenter = PreviewPresenter(self.mock_preview_view)
        prev_presenter.register_master(self.mock_master_presenter)

        prev_presenter.notify(Command.ELEMENTSELECTION)

        self.mock_preview_view.get_selected_item.assert_called_once()
