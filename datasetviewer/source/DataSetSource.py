class DataSetSource(object):

    def __init__(self, data):
        self.data = data

    def get_element(self, name):
        return self.data[name]

    def get_data(self):
        return data
