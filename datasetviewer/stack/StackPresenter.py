from datasetviewer.stack.interfaces.StackPresenterInterface import StackPresenterInterface
from datasetviewer.mainview.interfaces.MainViewPresenterInterface import MainViewPresenterInterface

class StackPresenter(StackPresenterInterface):
    """ StackPresenter that controls that appearance/disappearance of the various DimensionViews depending on which
    key has been selected in the PreviewView.

    Args:
        stack_view (StackView): Instance of a StackView.
        dim_fact (DimensionViewFactory): A DimensionViewFactory for creating the DimensionViews that populate the Stack.

    Private Attributes:
        _view (StackView): StackView associated with this Presenter. Assigned during initialisation.
        _dim_fact (DimensionViewFactory): DimensionViewFactory associated with this Presenter. Assigned during
            initialisation.
        _dict (DataSet): OrderedDict of xarray Datasets. Defaults to None. Assigned in `set_dict` method after file
            loading.
        _master (MainViewPresenter): Central Presenter that managed interaction between this and other Presenters.
            Defaults to None. Assigned in `register_master` method.
        _dim_presenters (Dictionary): Dictionary for storing the DimensionViews for all of the Dimensions contained in
            the dataset. Defaults to an empty dictionary as is populated during `set_dict`.
        _current_face (str): The key corresponding with the dataset that has been most recently selected in the
            PreviewView. Defaults to None and is assigned to the first key in the dataset in the `set_dict` method.
            Changed during calls to `set_current_face` when a message is received from the PreviewPresenter indicating
            a different dictionary element has been selected.

    Raises:
        ValueError: If the StackView or the DimensionViewFactory are None.
    """

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
        self._stack_idx = {}

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
        """

        Assign the _dict variable in the StackPresenter and create the required number of DimensionViews and elements
        on the StackPresenter.

        Args:
            dict (DataSet): An OrderedDict of xarray Datasets.

        """

        self._dict = dict

        # Clear the DimensionViews that were on the Stack
        self._clear_stack()

        self._dim_presenters = {}
        self._stack_idx = {}

        for key in dict.keys():

            # Create a new Stack element for every dataset in the dictionary
            idx = self._view.create_stack_element()
            self._stack_idx[key] = idx
            self._dim_presenters[key] = {}
            data = dict[key].data

            # Ignore data with a single dimension as they will not need DimensionViews
            if len(data.dims) > 1:

                for i in range(len(data.dims)):

                    # Create a widget for ever dimension in the dataset
                    w = self._dim_fact.create_widget(data.dims[i], data.shape[i])

                    # Obtain the presenter for the widget
                    self._dim_presenters[key][data.dims[i]] = w.get_presenter()

                    # Store the presenter in a dictionary
                    self._dim_presenters[key][data.dims[i]].register_stack_master(self)

                    # Place the widget in the Stack
                    self._view.add_dimension_view(idx, w)

        first_key = list(dict.keys())[0]

        print(self._stack_idx)

        # Set the current 'face' of the Stack to correspond with the first element in the dataset
        self.change_stack_face(first_key)

    def create_default_button_press(self, key):
        """

        Create the default button-configuration for the starting plot upon loading data or changing the dictionary
        element in the PreviewView. For 1D data this does nothing. For 2D data this selects the first dimension as the X
        axis and creates a 1D plot. For data with 3+ dimensions this selects the first dimension as the X axis, the
        second dimension as the Y axis, and creates a 2D plot. The sliders/steppers are enabled or disabled
        accordingly.

        """

        dataset = self._dict[key].data

        # Find the number of dimensions in the first dataset
        n_dims = len(dataset.dims)

        # Data has a single dimension - No need to configure buttons as they shouldn't exist
        if n_dims == 1:
            return

        # Data has two dimensions - Press the first X button
        elif n_dims == 2:

            self._dim_presenters[key][dataset.dims[0]].set_x_state(True)
            self._dim_presenters[key][dataset.dims[0]].set_y_state(False)
            self._dim_presenters[key][dataset.dims[0]].disable_dimension()

            self._dim_presenters[key][dataset.dims[1]].enable_dimension()

        # Data has three or more dimensions - Press the first X button and the second Y button
        else:

            self._dim_presenters[key][dataset.dims[0]].set_x_state(True)
            self._dim_presenters[key][dataset.dims[0]].disable_dimension()

            self._dim_presenters[key][dataset.dims[1]].set_y_state(True)
            self._dim_presenters[key][dataset.dims[1]].disable_dimension()

        for dim_name in self._dim_presenters[key].keys():

            if dim_name in [dataset.dims[0], dataset.dims[1]]:
                continue

            self._dim_presenters[key][dim_name].enable_dimension()

    def change_stack_face(self, key):
        """

        Change the visible face on the StackPresenter and create the default plot for that key. Called when a different
        element has been selected on the PreviewPresenter.

        Args:
            key (str): They key that the StackPresenter should change to.

        """

        self._view.change_stack_face(self._stack_idx[key])
        self._current_face = key
        self.create_default_button_press(key)

    def x_button_change(self, recent_x_button, state):
        """

        Manage the DimensionView changes when a new X button is checked and release the previous X button to ensure
        that only one is checked at a time.

        Args:
            recent_x_button (str): The name of the dimension for the most recently checked X button.
            state (bool): The state of the X button now has as a result of the press. Should always be True as X
                buttons should not be unselected.

        Raises:
            ValueError: If an unexpected number of X or Y buttons have been checked. Ideally this will be prevented from
                happening in the DimensionPresenter.

        """

        # Create a set containing the names of the dimensions for which an X or Y button has been checked.
        dims_with_x_checked = self._dims_with_x_checked()
        dims_with_y_checked = self._dims_with_y_checked()

        '''
        Raise an Exception if the number of X buttons checked is not equal to 2.
        '''
        if len(dims_with_x_checked) != 2:
            raise ValueError("Error: Too many or too few X buttons checked: " + str(dims_with_x_checked))

        num_dims_with_y_checked = len(dims_with_y_checked)

        '''
        Determine the name of the previous X button. This is found by taking the set of all X buttons that have been
        checked minus a set containing only the latest X button to be checked.
        '''
        previous_x_button = dims_with_x_checked - set(recent_x_button)
        previous_x_button = previous_x_button.pop()

        # Release the previous X button and enable its slider and stepper
        self._dim_presenters[self._current_face][previous_x_button].enable_dimension()

        # Disable the slider and stepper of the most recent X button to be checked.
        self._dim_presenters[self._current_face][recent_x_button].disable_dimension()

        # No Y buttons checked- Create a 1D plot
        if num_dims_with_y_checked == 0:

            self._master.create_onedim_plot(self._current_face,
                                            recent_x_button,
                                            self._create_slice_dictionary())

        # Single Y button checked - Create a 2D plot
        elif num_dims_with_y_checked == 1:

            self._master.create_twodim_plot(self._current_face,
                                            recent_x_button,
                                            dims_with_y_checked.pop(),
                                            self._create_slice_dictionary())

        # Two or more Y buttons checked - Raise an Exception
        else:
            raise ValueError("Error: Too many Y buttons checked: " + str(num_dims_with_y_checked))

    def y_button_change(self, recent_y_button, state):
        """

        Manage the plot change when the state of a Y button changes. This may involve releasing a previous Y button.
        Having zero Y buttons checked is permitted as this leads to the creation of a 1D plot.

        Args:
            recent_y_button (str): The name of the dimension for the Y button that had its state change.
            state (bool): The present state of the Y button as a result of the change. May be True or False as a Y
                button may be unselected to allow the user to switch between 2D plot and 1D plots.

        Raises:
            ValueError: If an unexpected number of X or Y buttons have been checked. Ideally this will be prevented from
                happening in the DimensionPresenter.

        """

        dims_with_x_checked = self._dims_with_x_checked()
        dims_with_y_checked = self._dims_with_y_checked()

        num_dims_with_y_checked = len(dims_with_y_checked)

        # Raise an Exception if the number of X buttons checked has any value other than 1
        if len(dims_with_x_checked) != 1:
            raise ValueError("Error: Too many or too few X buttons checked: " + str(dims_with_x_checked))

        # No Y buttons checked - Create a 1D plot
        if num_dims_with_y_checked == 0:

            # Release the recent Y button as this state change indicates that the button was unchecked
            self._dim_presenters[self._current_face][recent_y_button].enable_dimension()

            self._master.create_onedim_plot(self._current_face,
                                            dims_with_x_checked.pop(),
                                            self._create_slice_dictionary())

        # One Y button checked - Go from a 1D to a 2D plot. No need to release previous Y button.
        elif num_dims_with_y_checked == 1:

            # Disable the Y button as this state change indicates the button was checked
            self._dim_presenters[self._current_face][recent_y_button].disable_dimension()

            self._master.create_twodim_plot(self._current_face,
                                            dims_with_x_checked.pop(),
                                            recent_y_button,
                                            self._create_slice_dictionary())

        # Two Y buttons checked - Change the 2D plot. Must release previous Y button.
        elif num_dims_with_y_checked == 2:

            '''
            Determine the name of the previous Y button. This is found by taking the set of all Y buttons that have been
            checked minus a set containing only the latest Y button to be checked.
            '''
            previous_y_button = dims_with_y_checked - set(recent_y_button)
            previous_y_button = previous_y_button.pop()

            # Disable the DimensionView elements for the most recent Y button to be checked
            self._dim_presenters[self._current_face][recent_y_button].disable_dimension()

            # Enable the DimensionView elements for the previous Y button that was checked
            self._dim_presenters[self._current_face][previous_y_button].enable_dimension()

            self._master.create_twodim_plot(self._current_face,
                                            dims_with_x_checked.pop(),
                                            recent_y_button,
                                            self._create_slice_dictionary())

        # More than two Y buttons checked - Raise an Exception
        else:
            raise ValueError("Error: Too many Y buttons checked: " + str(num_dims_with_y_checked))

    def slice_change(self):
        """ Instruct the MainViewPresenter to draw a new plot when a slider/stepper value has been changed. """

        dims_with_x_checked = self._dims_with_x_checked()
        dims_with_y_checked = self._dims_with_y_checked()

        if len(dims_with_y_checked) == 0:

            self._master.create_onedim_plot(self._current_face,
                                            dims_with_x_checked.pop(),
                                            self._create_slice_dictionary())

        else:

            self._master.create_twodim_plot(self._current_face,
                                            dims_with_x_checked.pop(),
                                            dims_with_y_checked.pop(),
                                            self._create_slice_dictionary())

    def _dims_with_x_checked(self):
        """
        Find the dimensions that have their X button checked.

        Returns:
            set: A set of the names of the dimensions that have a checked X button.
        """

        return {dimname for dimname in self._dim_presenters[self._current_face].keys()
                if self._dim_presenters[self._current_face][dimname].get_x_state()}

    def _dims_with_y_checked(self):
        """
        Find the dimensions that have their Y button checked.

        Returns:
            set: A set of the names of the dimensions that have a checked Y button.
        """

        return {dimname for dimname in self._dim_presenters[self._current_face].keys()
                if self._dim_presenters[self._current_face][dimname].get_y_state()}

    def _create_slice_dictionary(self):
        """
        Find the slider values of the dimensions for which no buttons are checked.

        Returns:
            dict: A dictionary consisting of elemenets with a dimension name as the dictionary key and the slider value
                as the dictionary value.
        """

        return {dimname : self._dim_presenters[self._current_face][dimname].get_slider_value()
                for dimname in self._dim_presenters[self._current_face].keys()
                if self._dim_presenters[self._current_face][dimname].is_enabled() }

    def _clear_stack(self):

        for idx in range(self._view.count() - 1, -1, -1):
            self._view.delete_widget(idx)
