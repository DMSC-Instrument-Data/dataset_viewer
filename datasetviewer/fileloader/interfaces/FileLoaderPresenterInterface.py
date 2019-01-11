from abc import ABC, abstractmethod

class FileLoaderPresenterInterface(ABC):

    @abstractmethod
    def register_master(self, master):
        pass

    @abstractmethod
    def notify(self, command):
        pass

    @abstractmethod
    def _load_data(self, file_path):
        pass
