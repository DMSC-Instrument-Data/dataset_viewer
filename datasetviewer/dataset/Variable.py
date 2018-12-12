class Variable(object):

    def __init__(self, name, data):
        self.name = name
        self.data = data

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

    def get_dimensions(self):
        return self._data.shape
