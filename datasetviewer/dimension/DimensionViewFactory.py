from datasetviewer.dimension.interfaces.DimensionViewFactoryInterface import DimensionViewFactoryInterface
from datasetviewer.dimension.DimensionWidgets import DimensionWidgets

class DimensionViewFactory(DimensionViewFactoryInterface):
    """ Basic Factory for creation DimensionWidgets objects. """

    def __init__(self):
        pass

    def create_widget(self, dim_name, dim_size):
        """

        Create a DimensionWidgets object based on the name and size of a dimension.

        Args:
            dim_name (str): The name of the dimension. Required for creating the label.
            dim_size (int): The size of the dimension. Required for setting up the slider and stepper.

        Raises:
            DimensionWidgets: A DimensionWidgets object that owns a label, two buttons, a slider, and a stepper.

        """
        return DimensionWidgets(dim_name, dim_size)
