from datasetviewer.stack.interfaces.StackPresenterInterface import StackPresenterInterface

class StackPresenter(StackPresenterInterface):

    def __init__(self, stack_view, dim_fact):

        if stack_view is None:
            raise ValueError("Error: Cannot create StackView when View is None.")

        if dim_fact is None:
            raise ValueError("Error: Cannot create DimensionViewFactory when View is None.")

        self._view = stack_view
        self._dim_fact = dim_fact
        self._master = None

    def register_master(self, master):

        self._master = master
        master.subscribe_stack_presenter(self)

    def set_dict(self, dict):
        pass
