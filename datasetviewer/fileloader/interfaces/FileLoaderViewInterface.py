from abc import ABC, abstractmethod

class FileLoaderViewInterface(ABC):

    @abstractmethod
    def get_selected_file_path(self):
        pass

    @abstractmethod
    def show_reject_file_message(self, error_msg):
        pass
