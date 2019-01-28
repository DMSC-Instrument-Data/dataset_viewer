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

            self._dim_presenters[first_key][first_dataset.dims[0]].set_x_state(True)
            self._dim_presenters[first_key][first_dataset.dims[0]].set_y_state(False)
            self._dim_presenters[first_key][first_dataset.dims[0]].disable_dimension()

            self._dim_presenters[first_key][first_dataset.dims[1]].enable_dimension()

        else:

            self._dim_presenters[first_key][first_dataset.dims[0]].set_x_state(True)
            self._dim_presenters[first_key][first_dataset.dims[0]].disable_dimension()

            self._dim_presenters[first_key][first_dataset.dims[1]].set_y_state(True)
            self._dim_presenters[first_key][first_dataset.dims[1]].disable_dimension()

        for dim_name in self._dim_presenters[first_key].keys():

            if dim_name in [first_dataset.dims[0], first_dataset.dims[1]]:
                continue

            self._dim_presenters[first_key][dim_name].enable_dimension()

    def change_stack_face(self, key):

        self._view.change_stack_face(key)
        self._current_face = key

    def x_button_press(self, dim_name, state):

        dims_with_x_pressed = self._dims_with_x_pressed()
        dims_with_y_pressed = self._dims_with_y_pressed()

        if len(dims_with_x_pressed) > 2 or not dims_with_x_pressed:
            raise ValueError("Error: Too many or too few X buttons pressed: " + str(dims_with_x_pressed))

        num_dims_with_y_pressed = len(dims_with_y_pressed)

        previous_x_button = dims_with_x_pressed - set(dim_name)
        previous_x_button = previous_x_button.pop()

        self._dim_presenters[self._current_face][previous_x_button].enable_dimension()

        self._dim_presenters[self._current_face][dim_name].disable_dimension()

        if num_dims_with_y_pressed == 0:

            self._master.create_onedim_plot(self._current_face,
                                            dim_name,
                                            self._create_slice_dictionary())

        elif num_dims_with_y_pressed == 1:

            self._master.create_twodim_plot(self._current_face,
                                            dim_name,
                                            dims_with_y_pressed.pop(),
                                            self._create_slice_dictionary())

        else:
            raise ValueError("Error: Too many Y buttons pressed: " + str(num_dims_with_y_pressed))

    def y_button_press(self, dim_name, state):

        dims_with_x_pressed = self._dims_with_x_pressed()
        dims_with_y_pressed = self._dims_with_y_pressed()

        num_dims_with_y_pressed = len(dims_with_y_pressed)

        if len(dims_with_x_pressed) > 1 or not dims_with_x_pressed:
            raise ValueError("Error: Too many X or too few X buttons pressed: " + str(dims_with_x_pressed))

        if num_dims_with_y_pressed == 0:

            self._dim_presenters[self._current_face][dim_name].enable_dimension()

            self._master.create_onedim_plot(self._current_face,
                                            dims_with_x_pressed.pop(),
                                            self._create_slice_dictionary())

        elif num_dims_with_y_pressed == 1:

            self._dim_presenters[self._current_face][dim_name].disable_dimension()

            self._master.create_twodim_plot(self._current_face,
                                            dims_with_x_pressed.pop(),
                                            dim_name,
                                            self._create_slice_dictionary())

            return

        elif num_dims_with_y_pressed == 2:

            previous_y_button = dims_with_y_pressed - set(dim_name)
            previous_y_button = previous_y_button.pop()

            self._dim_presenters[self._current_face][dim_name].disable_dimension()

            self._dim_presenters[self._current_face][previous_y_button].enable_dimension()

            self._master.create_twodim_plot(self._current_face,
                                            dims_with_x_pressed.pop(),
                                            dim_name,
                                            self._create_slice_dictionary())

        else:
            raise ValueError("Error: Too many Y buttons pressed: " + str(num_dims_with_y_pressed))

    def slice_change(self):
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
