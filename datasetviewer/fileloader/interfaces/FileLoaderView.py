from abc import ABC, abstractmethod

class FileLoaderView(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def get_selected_file_path(self):
        pass

    @abstractmethod
    def file_selected(self):
        pass
