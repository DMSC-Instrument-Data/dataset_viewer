class Variable(object):

    def __init__(self, name, data):

        self._name = name
        self._data = data

    @property
    def name(self):
        return self._name

    @property
    def data(self):
        return self._data

    def get_dimensions(self):
        return self._data.shape
