from datasetviewer.dimension.interfaces.DimensionViewFactoryInterface import DimensionViewFactoryInterface
from datasetviewer.dimension.DimensionWidget import DimensionWidget

class DimensionViewFactory(DimensionViewFactoryInterface):
    """ Factory Method realisation for creating DimensionWidget QtWidgets. """

    def __init__(self, parent):
        self.parent = parent

    def create_widgets(self, dim_name, dim_size):
        """

        Create a DimensionWidgets object based on the name and size of a dimension.

        Args:
            dim_name (str): The name of the dimension. Required for creating the label.
            dim_size (int): The size of the dimension. Required for setting up the slider and stepper.

        Returns:
            DimensionWidget: A DimensionWidgets object that consists of a label, two buttons, a slider, and a stepper.

        """
        return DimensionWidget(dim_name, dim_size, self.parent)
