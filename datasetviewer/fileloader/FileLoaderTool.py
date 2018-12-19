from xarray import open_dataset
from collections import OrderedDict as DataSet
from datasetviewer.dataset.Variable import Variable

class FileLoaderTool(object):
    """ Tool for opening an ncs file and converting it to an OrderedDict of Variable objects. """

    def __init__(self):
        pass

    def invalid_dataset(self, data):
        """
        Determines if a data array is suitable for plotting by checking the number of dimensions in all of its elements.
        An element with only one dimension will cause the entire dataset to be rejected.

        Args:
            data (xarray.core.utils.Dataset): An xarray dataset.

        Returns:
            bool: True if any of the elements have less than two dimensions, False otherwise.

        """

        for key in data.variables:
            if len(data[key].sizes) < 2:
                return True

        return False

    def dataset_to_dict(self, data):
        """
        Converts a dataset from xarray format to an OrderedDict of Variables.

        Args:
            data (xarray.core.dataset.Dataset): An xarray dataset.

        Returns:
            DataSet: The xarray data in the form of an OrderedDict.

        """

        dataset = DataSet()

        for key in data.variables:
            dataset[key] = Variable(key, data[key])

        return dataset

    def file_to_dict(self, file_path):
        """
        Loads the data from a file path and converts it to a dictionary.

        Args:
            file_path (str): The path of the file to be opened.

        Raises:
            ValueError: If the dataset is empty, or if any of its elements only have a single dimension.
            TypeError: If the file could not be converted to the an xarray.

        Returns:
            DataSet: An OrderedDict of Variable objects containing a name and a data array.

        """

        data = open_dataset(file_path)

        if len(data.variables) < 1:
            raise ValueError("Error in FileLoader: Dataset is empty.")

        if self.invalid_dataset(data):
            raise ValueError("Error in FileLoader: Dataset contains one or more elements with <2 dimensions.")

        return self.dataset_to_dict(data)
