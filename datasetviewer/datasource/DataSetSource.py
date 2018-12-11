from abc import abstractmethod

class DataSetSource(object):

    def __init__(self):
        pass

    @abstractmethod
    def get_element(self, name):
        pass

    @abstractmethod
    def get_data(self):
        pass
