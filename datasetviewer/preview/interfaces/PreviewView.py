from abc import ABC, abstractmethod


class PreviewView(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def add_entry_to_list(self, entry_text):
        pass
