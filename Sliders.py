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

    def __init__(self):

        super().__init__()

        # Collection of letters used to create random dimension names
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        # Set number of dimension
        self.n_dims = 7

        # Create empty dictionary for slice selection
        self.slice_selection = {}

        # Generate random dimension names and sizes
        self.dim_names = [alphabet[i] for i in sample(range(26),self.n_dims)]
        self.dim_sizes = {self.dim_names[i]: randint(2,10) for i in range(self.n_dims)}

        # Create a list of Dimension objects
        self.dims = [Dimension(self.dim_names[i],self.dim_sizes[self.dim_names[i]],i) for i in range(self.n_dims)]

        # Create a random n-D array
        self.arr = np.random.rand(*[self.dim_sizes[key] for key in self.dim_names])
        self.xarr = xr.DataArray(self.arr, dims = self.dim_names)

        # Print dimension name and size
        print("Dimension sizes: ")
        print(self.xarr.sizes)

        # Create a figure
        self.figure = Figure()

        # Create an axis object
        self.ax = self.figure.add_subplot(1,1,1)

        # Create a layout
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        layout = QGridLayout(self._main)

        # Create a FigureCanvas
        self.canvas = FigureCanvas(self.figure)

        # Add the canvas to the layout
        height_plot = 1
        width_plot = 6
        layout.addWidget(self.canvas,0,0,height_plot,width_plot)
        self.addToolBar(NavigationToolbar(self.canvas, self))

        # Offset to make space for the log/linear buttons 
        shift = 2

        # Buttons for setting plot scale
        self.lin_button = QRadioButton("Linear")
        self.log_button = QRadioButton("Log")

        self.lin_button.setChecked(True)

        self.lin_button.toggled.connect(lambda: self.change_scale('linear'))
        self.log_button.toggled.connect(lambda: self.change_scale('log'))

        layout.addWidget(self.lin_button,1,4)
        layout.addWidget(self.log_button,1,5)

        for dim in self.dims:

            # Create a label
            dim.create_label()

            # Create X and Y buttons for the slider
            x_func = self.press_button(dim,0,1)
            y_func = self.press_button(dim,1,0)
            dim.create_buttons(x_func,y_func)

            # Create a slider
            dim.create_slider(self.slider_changer_creator(dim))

            # Create a stepper
            dim.create_stepper(self.stepper_changer_creator(dim))

            # Add the buttons and slider to the box
            layout.addWidget(dim.label, dim.no+shift, 0)
            layout.addWidget(dim.buttons[0], dim.no+shift, 1)
            layout.addWidget(dim.buttons[1], dim.no+shift, 2)
            layout.addWidget(dim.slider, dim.no+shift, 3)
            # Have the slider take up two 'cells' so the log/linear buttons are not pushed too far apart
            layout.addWidget(dim.stepper, dim.no+shift, 4,1,2)

        # Prepare the initial view (last two dimensions are set to X and Y)
        self.prepare_initial_view()

    def prepare_initial_view(self):

	# Use the first value of the first n - 2 dimensions for the as the initial slices
        for i in range(self.n_dims - 2):
            self.slice_selection[self.dim_names[i]] = 0

        # Set the last two dimensions as the x and y axes
        self.axes = [self.dims[-2], self.dims[-1]]

        # Reshape the array for the initial configuration
        self.arr = self.xarr.isel(self.slice_selection).transpose(self.dim_names[-1],self.dim_names[-2])

        # Check the X and Y buttons for the initial axes setup
        self.axes[0].buttons[0].setChecked(True)
        self.axes[1].buttons[1].setChecked(True)

        # Disable their sliders and steppers
        for dim in self.axes:

            dim.slider.setVisible(False)
            dim.stepper.setVisible(False)

        # Plot the array
        self.im = self.ax.imshow(self.arr)
        self.cbar = self.figure.colorbar(self.im)

        # Label the axes
        self.ax.set_xlabel(self.axes[0].name)
        self.ax.set_ylabel(self.axes[1].name)

    def change_scale(self, scale):

        if scale == 'log':
            self.im.set_norm(LogNorm(*self.get_minmax()))
        else:
            self.im.set_norm(Normalize())

        # Draw the canvas
        self.cbar.draw_all()
        self.canvas.draw()

    def press_button(self, dim, curr_axis_no, neighb_axis_no):

        def slice_changer():

           # Ignore the instruction if another dimension has already been selected for the same axis
            if self.axis_already_selected(dim,curr_axis_no):
                dim.buttons[curr_axis_no].setChecked(False)
                return

            # Set this dimension as an axes
            if dim.buttons[curr_axis_no].isChecked():

                # Disable the matching slider and stepper
                dim.slider.setVisible(False)
                dim.stepper.setVisible(False)

                # Switch off the neighbouring button
                dim.buttons[neighb_axis_no].setChecked(False)

                # Set current axis to this dimension
                self.axes[curr_axis_no] = dim

                # Remvoe this dimension from the slice dictionary
                self.slice_selection.pop(dim.name, None)

                # Change the view if both a X and a Y axis have been selected
                if self.num_buttons_pressed() == 2:
                    self.change_view()

            # Unset this dimension as an axis
            else:

                # Enable the matching slider and stepper
                dim.slider.setVisible(True)
                dim.stepper.setVisible(True)

                # Set current axis to None
                self.axes[curr_axis_no] = None

                # Place this dimension in the slice dictionary
                self.slice_selection[dim.name] = 0

        return slice_changer

    def axis_already_selected(self,curr_dim,n_curr_axis):

        # Check that the same axis has already been selected elsewhere (i.e., prevent to difference X buttons from being checked at the same time)
        for dim in self.dims:
            if dim.buttons[n_curr_axis].isChecked() and dim != curr_dim:
                return True
        return False

    def stepper_changer_creator(self,dim):

        # Sequence to be carried out when the stepper detects a change
        def stepper_changer():

            # Don't change the slider/stepper value if less than two buttons have been pressed
            if self.num_buttons_pressed() <= 1:
                self.revert_value_change(dim)
                return

            # Obtain the stepper value
            stepper_val = dim.stepper.value()

            # Change slider value to match the stepper
            dim.slider.setValue(stepper_val)

            # Update the slice selection dictionary
            self.slice_selection[dim.name] = stepper_val

            # Change the view
            self.change_view()

        return stepper_changer

    def slider_changer_creator(self,dim):

        # Sequence to be carried out when the slider detects a change
        def slider_changer():

            # Don't change the slider/stepper value if less than two buttons have been pressed
            if self.num_buttons_pressed() <= 1:
                self.revert_value_change(dim)
                return

            # Obtain the slider value
            slider_val = dim.slider.value()

            # Change the stepper value to match the slider
            dim.stepper.setValue(slider_val)

            # Update the slice selection dictionary
            self.slice_selection[dim.name] = slider_val

            # Change the view
            self.change_view()

        return slider_changer

    def revert_value_change(self, dim):

        # Go back to the previous slider/stepper values when a change isn't wanted
        #
        dim.slider.setValue(self.slice_selection[dim.name])
        dim.stepper.setValue(self.slice_selection[dim.name])

    def change_view(self):

        # Create a 2D array
        self.arr = self.xarr.isel(self.slice_selection).transpose(self.axes[1].name,self.axes[0].name)

        # Plot the reshaped array
        self.im.set_data(self.arr)
        print(type(self.im))

        # Label the axes
        self.ax.set_xlabel(self.axes[0].name)
        self.ax.set_ylabel(self.axes[1].name)

        # Update the colourbar
        self.im.set_clim(*self.get_minmax())
        self.cbar.draw_all()

        # Draw the canvas
        self.canvas.draw()

    def get_minmax(self):

        # Find the minimum and maximum values of the current array
        min_val = self.arr.min().values
        max_val = self.arr.max().values

        return [min_val,max_val]

    def num_buttons_pressed(self):

        # Count the number of axis button that have been pressed
        # Used to prevent X being pressed for two different dimensions, etc
        n_buttons_pressed = 0

        for dim in self.dims:
            if any([button.isChecked() for button in dim.buttons]):
                n_buttons_pressed += 1

        return n_buttons_pressed

if __name__ == "__main__":
    qapp = QtWidgets.QApplication(sys.argv)
    app = ApplicationWindow()
    app.show()
    qapp.exec_()
