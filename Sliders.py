import sys
import numpy as np
import xarray as xr
from random import randint, sample
from matplotlib.colors import LogNorm, Normalize

from PyQt5.QtWidgets import QGridLayout, QRadioButton

from matplotlib.backends.qt_compat import QtWidgets, is_pyqt5
if is_pyqt5():
    from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
else:
    from matplotlib.backends.backend_qt4agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure

from Dimension import Dimension

class ApplicationWindow(QtWidgets.QMainWindow):

    def __init__(self,n_dims,dim_names,dims,xarr):

        if n_dims < 2:
            raise Exception("Data does not have enough dimensions.")

        super().__init__()

        self.n_dims = n_dims
        self.dim_names = dim_names
        self.dims = dims
        self.xarr = xarr

        # Create empty dictionary for slice selection
        self.slice_selection = {}

        # Print dimension name and size
        print("Dimension sizes: ")
        print(self.xarr.sizes)

        # Create plot components
        self.figure = Figure()
        self.ax = self.figure.add_subplot(1, 1, 1)
        self.canvas = FigureCanvas(self.figure)

        # Create the layout
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        layout = QGridLayout(self._main)

        # Define grid size
        plot_cols = 6
        plot_rows = 1

        # Have the plot take up one row and multiple columns so it fills the window
        layout.addWidget(self.canvas,1,0,plot_rows,plot_cols)
        self.addToolBar(NavigationToolbar(self.canvas, self))

        # Offset to make space for the log/linear buttons
        shift = 2

        # Buttons for setting plot scale
        self.lin_button = QRadioButton("Linear")
        self.log_button = QRadioButton("Log")

        # Starting scale for initial plot
        self.curr_scale = 'linear'
        self.lin_button.setChecked(True)

        # Functions for the Linear/Log buttons
        self.lin_button.toggled.connect(lambda: self.change_scale('linear'))
        self.log_button.toggled.connect(lambda: self.change_scale('log'))

        # Insert log/linear buttons in top row of GridLayout
        layout.addWidget(self.lin_button,0,4)
        layout.addWidget(self.log_button,0,5)

        for dim in self.dims:

            # Create dimension label that appears to the left of the button
            dim.create_label()

            # Create X and Y buttons for the slider
            x_func = self.press_button(dim,0,1)
            y_func = self.press_button(dim,1,0)
            dim.create_buttons(x_func,y_func)

            # Create a slider
            dim.create_slider([self.stepper_changer_creator(dim), self.change_view])

            # Create a stepper
            dim.create_stepper([self.stepper_changer_creator(dim), self.change_view])

            # Add dimension components to the layout
            layout.addWidget(dim.label, dim.no+shift, 0)
            layout.addWidget(dim.buttons[0], dim.no+shift, 1)
            layout.addWidget(dim.buttons[1], dim.no+shift, 2)
            layout.addWidget(dim.slider, dim.no+shift, 3)

            # Have the slider take up two 'cells' so the log/linear buttons are not pushed too far apart
            layout.addWidget(dim.stepper, dim.no+shift, 4,1,2)

        # Dictionary of norms to use when log/linear button is pressed
        self.norms = {'log': None, 'linear': Normalize()}

        # Prepare the initial view (this sets the last two dimensions as X and Y)
        self.prepare_initial_view()

    def prepare_initial_view(self):

    # Use the first value of the first n - 2 dimensions for the as the initial slices
        for i in range(self.n_dims - 2):
            self.slice_selection[self.dim_names[i]] = 0

        # Set the last two dimensions as the x and y axes
        self.axes = [self.dims[-2], self.dims[-1]]

        # Check the X and Y buttons for the initial axes setup
        self.axes[0].buttons[0].setChecked(True)
        self.axes[1].buttons[1].setChecked(True)

        # Disable sliders and steppers of the last two dimensions
        for dim in self.axes:

            dim.slider.setVisible(False)
            dim.stepper.setVisible(False)

        # Create the slice array
        self.create_twodim_array()

        # Create the axis plot and colourbar
        self.im = self.ax.imshow(self.arr)
        self.cbar = self.figure.colorbar(self.im)

        self.label_axes()

    def change_scale(self, scale):

        # Update current scale
        self.curr_scale = scale

        try:
            # Try to change the scale of the colormap plot
            self.im.set_norm(self.norms[scale])
            self.update_colourbar()
        except:
            # Exception occurs becase colormap does not exist - instead change the scale of the 1D plot
            self.ax.set_yscale(scale)

        self.canvas.draw()

    def update_colourbar(self):

        # Remove previous colorbar and create a new updated one
        self.cbar.remove()
        self.cbar = self.figure.colorbar(self.im)

    def press_button(self, dim, curr_axis_no, neighb_axis_no):

        def slice_changer():

           # Ignore the instruction if another dimension has already been selected for the same axis
            if self.axis_already_selected(dim,curr_axis_no):
                dim.buttons[curr_axis_no].setChecked(False)
                return

            # Set this dimension as an axes
            if dim.buttons[curr_axis_no].isChecked():

                # Disable the corresponding slider and stepper
                dim.slider.setVisible(False)
                dim.stepper.setVisible(False)

                # Switch off the neighbouring button
                dim.buttons[neighb_axis_no].setChecked(False)

            # Unset this dimension as an axis
            else:

                # Enable the matching slider and stepper
                dim.slider.setVisible(True)
                dim.stepper.setVisible(True)

            self.change_view()

        return slice_changer

    def axis_already_selected(self,curr_dim,n_curr_axis):

        # Check that the same axis has already been selected elsewhere (this prevents two different X buttons from being checked at the same time)
        for dim in self.dims:
            if dim.buttons[n_curr_axis].isChecked() and dim != curr_dim:
                return True
        return False

    def stepper_changer_creator(self, dim):

        # SeqUence to be carried out when the stepper detects a change
        def stepper_changer(value):

            # Change slider value to match the stepper
            dim.slider.setValue(value)

        return stepper_changer

    def slider_changer_creator(self, dim):

        # Sequence to be carried out when the slider detects a change
        def slider_changer(value):

            # Change the stepper value to match the slider
            dim.stepper.setValue(value)

        return slider_changer

    def get_slice_selection(self):

        # Rebuild the slice selection dictionary based on the current value of the sliders
        self.slice_selection = {}

        for dim in self.dims:
            # Ignore the dimensions that have been selected as an X/Y axis
            if not any([button.isChecked() for button in dim.buttons]):
                self.slice_selection[dim.name] = dim.slider.value()

    def update_axes(self):

        self.axes = [None, None]

        for dim in self.dims:
            for i in range(len(dim.buttons)):
                if dim.buttons[i].isChecked():
                    self.axes[i] = dim

    def change_view(self):

        # Determine the slice needed from the current value of the steppers
        self.get_slice_selection()

        self.clear_plot()

        # Do nothing if zero buttons are pressed
        if self.num_buttons_pressed() == 0 or not self.x_button_pressed():
            return

        # Create a 1D plot if a single X button has been pressed
        if self.num_buttons_pressed() == 1:

            self.create_onedim_array()
            self.line = self.ax.plot(self.arr,color='green')

            # Set the appropriate scale based on the status of the log/linear buttons
            self.ax.set_yscale(self.curr_scale)

            # Prevent the plot from being squashed
            self.ax.set_aspect('auto')

        # Create a colourmap plot if an X and a Y button have been pressed
        elif self.num_buttons_pressed() == 2:

            self.update_axes()
            self.create_twodim_array()
            self.im = self.ax.imshow(self.arr)

            # Set the appropriate scale based on the status of the log/linear buttons
            self.im.set_norm(self.norms[self.curr_scale])

            self.cbar = self.figure.colorbar(self.im)
            self.label_axes()

        self.canvas.draw()

    def x_button_pressed(self):

        # Check if any of the X buttons have been pressed for all dimension
        return any([dim.buttons[0].isChecked() for dim in self.dims])

    def clear_plot(self):

        # Try to delete a line plot if it exists
        try:
            self.line.pop(0).remove()
        except:
            # Exception - plot being displayed is a colourmap
            pass

        # Prevent next plot from taking shape of the previous plot
        try:
            self.ax.cla()
        except:
            pass

        # Try to delete a colourbar if it exists
        try:
            self.cbar.remove()
        except:
            pass

        # Try to delete a colormap if it exists
        try:
            self.im.remove()
        except:
            pass

    def create_onedim_array(self):

        self.arr = self.xarr.isel(self.slice_selection)

    def create_twodim_array(self):

        self.arr = self.xarr.isel(self.slice_selection).transpose(self.axes[1].name,self.axes[0].name)
        self.norms['log'] = LogNorm(*self.get_minmax())

    def label_axes(self):

        self.ax.set_xlabel(self.axes[0].name)
        self.ax.set_ylabel(self.axes[1].name)

    def get_minmax(self):

        '''
        Find the minimum and maximum values of the current array in order to configure the
        colourbar
        '''
        min_val = self.arr.min().values
        max_val = self.arr.max().values

        return [min_val, max_val]

    def num_buttons_pressed(self):

        # Count the number of axis button that have been pressed
        # Used to prevent X being pressed for two different dimensions
        n_buttons_pressed = 0

        for dim in self.dims:
            if any([button.isChecked() for button in dim.buttons]):
                n_buttons_pressed += 1

        return n_buttons_pressed

if __name__ == "__main__":

    # Collection of letters used to create random dimension names
    ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    # Set number of dimensions
    N_DIMS = 6

    # Generate random dimension names and sizes
    DIM_NAMES = [ALPHABET[i] for i in sample(range(26), N_DIMS)]
    DIM_SIZES = [randint(20, 30) for i in range(N_DIMS)]

    # Create a random n-D array
    ARR = np.random.rand(*[size for size in DIM_SIZES])
    XARR = xr.DataArray(ARR, dims=DIM_NAMES)

    # Create a list of Dimension objects
    DIMS = [Dimension(DIM_NAMES[i], DIM_SIZES[i], i) for i in range(N_DIMS)]

    QAPP = QtWidgets.QApplication(sys.argv)
    APP = ApplicationWindow(N_DIMS, DIM_NAMES, DIMS, XARR)
    APP.show()
    QAPP.exec_()
