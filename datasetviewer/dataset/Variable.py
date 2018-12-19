class Variable(object):
    """Data Structure for storing an array and a name/key.

    Args:
        name (str): The name/key associated with the data.
        data (xarray.core.variable.Variable): An xarray data structure that contains a key, dimension names, dimension
        sizes, and a data array with 2+ dimensions

    """

    def __init__(self, name, data):

        self._name = name
        self._data = data

    @property
    def name(self):
        """str: The name associated with the data/key array."""

        return self._name

    @property
    def data(self):
        """xarray.core.variable.Variable: An xarray data structure."""

        return self._data

    def get_dimensions(self):
        """
        Returns:
            tuple: The dimensions of the data array.

        """

        return self._data.shape
