import unittest
from unittest.mock import patch
import datasetviewer.fileloader.FileLoaderTool as FileLoaderTool

import xarray as xr
import numpy as np

class FileLoaderTest(unittest.TestCase):

    def setUp(self):

        # Bad data in which one of the elements is an empty array
        self.bad_data = xr.Dataset({'good': (['x', 'y', 'z'], np.random.rand(3, 4, 5)), 'bad': np.array([])})

        # Good data for which all of the elements have some data
        self.good_data = xr.Dataset({'good': (['x', 'y', 'z'], np.random.rand(3, 4, 5)),
                                     'valid': (['b'], np.random.rand(3)),
                                     'alsogood': (['c', 'd', 'e', 'f'], np.random.rand(3, 4, 5, 6))})

        self.fake_data_path = "madeuppath"

    def test_empty_file_throws(self):
        """
        Test that an empty data array is rejected by the FileLoaderTool.
        """
        empty_data = xr.Dataset()

        # Patch the `open_dataset` function so that it returns an empty data file
        with patch('datasetviewer.fileloader.FileLoaderTool.open_dataset', side_effect = lambda path: empty_data):

            with self.assertRaises(ValueError):
                FileLoaderTool.file_to_dict(self.fake_data_path)

    def test_bad_dimensions_rejected(self):
        """
        Test that a data array containing elements with no data is deemed invalid by the FileLoaderTool
        """
        self.assertTrue(FileLoaderTool.invalid_dataset(self.bad_data))

    def test_good_dimensions_accepted(self):
        """
        Test that a data array containing no empty elements is deemed valid by the FileLoaderTool.
        """
        self.assertFalse(FileLoaderTool.invalid_dataset(self.good_data))

    def test_file_read_success(self):
        """
        Test that FileLoaderTool calls the `open_dataset` function.
        """

        # Patch the `open_dataset` so that it returns good data
        with patch('datasetviewer.fileloader.FileLoaderTool.open_dataset', side_effect = lambda path: self.good_data) \
                as dummy_data_loader:

            '''
            Call the `file_to_dict` conversion function and check that this causes the `open_dataset` function to
            be called with the expected filepath
            '''
            FileLoaderTool.file_to_dict(self.fake_data_path)
            dummy_data_loader.assert_called_once_with(self.fake_data_path)

    def test_bad_data_raises(self):
        """
        Test that bad data being returned by the `open_dataset` function raises an Exception.
        """

        # Patch the `open_dataset` function so that it returns invalid data.
        with patch('datasetviewer.fileloader.FileLoaderTool.open_dataset', side_effect = lambda path: self.bad_data):
            with self.assertRaises(ValueError):
                FileLoaderTool.file_to_dict(self.fake_data_path)
