from xarray import open_dataset

class FileReader(object):

    def __init__(self):
        pass

    def invalid_dataset(self, data):
        pass

    def dataset_to_ordered_dict(self, dataset):
        pass

    def file_to_dataset(self, file_path):

        data = open_dataset(file_path)

        if self.invalid_dataset(data):
            raise ValueError()
