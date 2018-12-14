from xarray import open_dataset


class FileLoaderTool(object):

    def __init__(self):
        pass

    def invalid_dataset(self, data):

        for key in data.variables:
            if len(data[key].sizes) < 2:
                return True

        return False

    def file_to_dict(self, file_path):

        data = open_dataset(file_path)

        if len(data.variables) < 1:
            raise ValueError("Error in FileLoader: Dataset is empty.")

        if self.invalid_dataset(data):
            raise ValueError("Error in FileLoader: Dataset contains one or more elements with <2 dimensions.")

        return data.variables
