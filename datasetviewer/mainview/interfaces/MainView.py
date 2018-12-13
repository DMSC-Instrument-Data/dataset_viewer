from abc import ABC, abstractmethod


class MainView(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def get_selected_file_path(self):
        pass
