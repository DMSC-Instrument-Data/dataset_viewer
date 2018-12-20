from xarray import open_dataset
from collections import OrderedDict as DataSet
from datasetviewer.dataset.Variable import Variable

""" Tool for opening an ncs file and converting it to an OrderedDict of Variable objects. """

def invalid_dataset(data):
    """
    Determines if a data array is suitable for plotting by checking the contents of its elements. Empty arrays cause the
    function to return True.

    Args:
        data (xarray.core.utils.Dataset): An xarray dataset.

    Returns:
        bool: True if any of the elements are empty, False otherwise.

    """

    for key in data.variables:
        if len(data[key]) < 1:
            return True

    return False

def dataset_to_dict(data):
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

def file_to_dict(file_path):
    """
    Loads the data from a file path and converts it to a dictionary.

    Args:
        file_path (str): The path of the file to be opened.

    Raises:
        ValueError: If the dataset is empty, or if any of its elements are empty.
        TypeError: If the file could not be converted to the an xarray.

    Returns:
        DataSet: An OrderedDict of Variable objects containing a name and a data array.

    """

    data = open_dataset(file_path)

    if len(data.variables) < 1:
        raise ValueError("Error in FileLoader: Dataset is empty.")

    if invalid_dataset(data):
        raise ValueError("Error in FileLoader: Dataset contains some empty arrays.")

    return dataset_to_dict(data)
