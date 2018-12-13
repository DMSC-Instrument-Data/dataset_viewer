from xarray import open_dataset
from datasetviewer.dataset.Variable import Variable
from collections import OrderedDict as DataSet


class FileReader(object):

    def __init__(self):
        pass

    def invalid_dataset(self, data):

        for key in data.variables:
            if len(data[key].sizes) < 2:
                return True

        return False

    def file_to_dict(self, file_path):

        data = open_dataset(file_path)

        if self.invalid_dataset(data):
            raise ValueError("Error in FileReader: Dataset contains one or more elements with <2 dimensions.")

        return data.variables
