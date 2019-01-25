from datasetviewer.stack.interfaces.StackPresenterInterface import StackPresenterInterface
from datasetviewer.mainview.interfaces.MainViewPresenterInterface import MainViewPresenterInterface

class StackPresenter(StackPresenterInterface):

    def __init__(self, stack_view, dim_fact):

        if stack_view is None:
            raise ValueError("Error: Cannot create StackView when View is None.")

        if dim_fact is None:
            raise ValueError("Error: Cannot create DimensionViewFactory when View is None.")

        self._view = stack_view
        self._dim_fact = dim_fact
        self._dict = None
        self._master = None
        self._dim_presenters = {}
        self._current_face = None

    def register_master(self, master):
        """

        Register the MainViewPresenter as the StackPresenter's master, and subscribe the MainViewPresenter to the
        StackPresenter.

        Args:
            master (MainViewPresenter): An instance of a MainViewPresenter.

        """
        assert (isinstance(master, MainViewPresenterInterface))

        self._master = master
        master.subscribe_stack_presenter(self)

    def set_dict(self, dict):

        self._dict = dict
        self._view.clear_stack()

        for key in dict.keys():

            self._view.create_stack_element(key)
            self._dim_presenters[key] = {}
            data = dict[key].data

            if len(data.dims) > 1:

                for i in range(len(data.dims)):

                    w = self._dim_fact.create_widget(data.dims[i], data.shape[i])
                    self._dim_presenters[key][data.dims[i]] = w.get_presenter()
                    self._dim_presenters[key][data.dims[i]].register_stack_master(self)
                    self._view.add_dimension_view(key, w)

        self.change_stack_face(list(dict.keys())[0])
        self.create_default_button_press()

    def create_default_button_press(self):

        # Create the default plot once all the View elements have been prepared
        first_key = list(self._dict.keys())[0]
        first_dataset = self._dict[first_key].data
        n_dims = len(first_dataset.dims)

        if n_dims == 1:
            return

        elif n_dims == 2:
            self._view.press_x(first_key, first_dataset.dims[0])

        else:
            self._view.press_x(first_key, first_dataset.dims[0])
            self._view.press_y(first_key, first_dataset.dims[1])

    def change_stack_face(self, key):

        self._view.change_stack_face(key)
        self._current_face = key

    def x_button_press(self, dim_name, state):
        pass

    def y_button_press(self, dim_name, state):

        dims_with_x_pressed = self._dims_with_x_pressed()
        dims_with_y_pressed = self._dims_with_y_pressed()

        num_dims_with_y_pressed = len(dims_with_y_pressed)

        if num_dims_with_y_pressed == 0:

            self._dim_presenters[self._current_face][dim_name].enable_dimension()

            self._master.create_onedim_plot(self._current_face,
                                            dims_with_x_pressed.pop(),
                                            self._create_slice_dictionary())

            return

        if num_dims_with_y_pressed == 1:
            return

        if num_dims_with_y_pressed == 2:
            return

    def slider_change(self, dim_name, val):
        pass

    def stepper_change(self, dim_name, val):
        pass

    def _dims_with_x_pressed(self):

        return {dimname for dimname in self._dim_presenters[self._current_face].keys()
                if self._dim_presenters[self._current_face][dimname].get_x_state()}

    def _dims_with_y_pressed(self):

        return {dimname for dimname in self._dim_presenters[self._current_face].keys()
                if self._dim_presenters[self._current_face][dimname].get_y_state()}

    def _create_slice_dictionary(self):

        return {dimname : self._dim_presenters[self._current_face][dimname].get_slider_value()
                for dimname in self._dim_presenters[self._current_face].keys()
                if self._dim_presenters[self._current_face][dimname].is_enabled() }
