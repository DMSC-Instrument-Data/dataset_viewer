from abc import ABC, abstractmethod

class PreviewViewInterface(ABC):

    @abstractmethod
    def add_entry_to_list(self, entry_text):
        pass
