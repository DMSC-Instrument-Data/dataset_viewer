from abc import ABC, abstractmethod

class PreviewPresenterInterface(ABC):

    @abstractmethod
    def set_data(self, dict):
        pass

    @abstractmethod
    def register_master(self, master):
        pass

    @abstractmethod
    def _create_preview_text(self, name):
        pass

    @abstractmethod
    def _add_preview_entry(self, name):
        pass

    @abstractmethod
    def _populate_preview_list(self):
        pass

    @abstractmethod
    def notify(self, command):
        pass
