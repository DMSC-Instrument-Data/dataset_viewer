from datasetviewer.dimension.interfaces.DimensionViewFactoryInterface import DimensionViewFactoryInterface
from datasetviewer.dimension.DimensionWidgets import DimensionWidgets

class DimensionViewFactory(DimensionViewFactoryInterface):

    def __init__(self, parent = None):
        self.parent = parent

    def create_widget(self, dim_name, dim_size):
        return DimensionWidgets(dim_name, dim_size)
