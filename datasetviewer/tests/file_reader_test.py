import unittest
from datasetviewer.fileloader.FileReader import FileReader

import xarray as xr
import numpy as np

class FileReaderTest(unittest.TestCase):

    def setUp(self):
        self.file_reader = FileReader()

    def test_empty_file_throws(self):
        # Test that a file that contains an empty dictionary isn't accepted
        pass

    def test_bad_dimensions(self):

        bad_data = xr.Dataset({'good': (['x', 'y', 'z'], np.random.rand(3, 4, 5)), 'bad': np.random.rand(2)})

        self.assertTrue(self.file_reader.invalid_dataset(bad_data))

    def test_good_dimensions(self):

        good_data = xr.Dataset({'good': (['x', 'y', 'z'], np.random.rand(3, 4, 5)),  'alsogood': (['a', 'b', 'c', 'e'], np.random.rand(3, 4, 5, 6))})

        self.assertFalse(self.file_reader.invalid_dataset(good_data))
