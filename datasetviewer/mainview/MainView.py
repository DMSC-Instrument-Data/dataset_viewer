from abc import abstractmethod

class MainView(object):

    def __init__(self):
        pass

    @abstractmethod
    def get_selected_file_path(self):
        pass
