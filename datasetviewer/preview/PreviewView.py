from abc import abstractmethod

class PreviewView(object):

    def __init__(self):
        pass

    @abstractmethod
    def register_master(self):
        pass

    @abstractmethod
    def add_entry_to_list(self, entry_text):
        pass
