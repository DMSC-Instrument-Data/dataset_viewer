import numpy as np
from numpy import resize
import xarray as xr
import hvplot.xarray
import holoviews as hv
from random import randint, sample

import sys
 
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton, QSlider, QHBoxLayout, QGridLayout, QLabel, QSpinBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt,  QCoreApplication
 
import sys
import time

import numpy as np

from Dimension import Dimension

import matplotlib.pyplot as plt

from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
if is_pyqt5():
    from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
else:
    from matplotlib.backends.backend_qt4agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure

renderer = hv.renderer('matplotlib')
    
class ApplicationWindow(QtWidgets.QMainWindow):

    def __init__(self):
    
        super().__init__()

        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        self.n_dims = 7 

        self.slice_selection = {}

        self.dim_names = [alphabet[i] for i in sample(range(26),self.n_dims)] 
        self.dim_sizes = {self.dim_names[i]: randint(2,10) for i in range(self.n_dims)}

        print(" \ ".join([self.dim_names[i] + ": " + str(self.dim_sizes[self.dim_names[i]]) for i in range(self.n_dims)]))

        self.dims = [Dimension(self.dim_names[i],self.dim_sizes[self.dim_names[i]],i) for i in range(self.n_dims)] 

        # Create a random 2D array
        self.arr = np.random.rand(*[self.dim_sizes[key] for key in self.dim_names])
        self.xarr = xr.DataArray(self.arr, dims = self.dim_names)

        print("Initial axis selection:")
        print(self.slice_selection)
        # print(type(fig.plot()))
 
        # Create a figure
        self.figure = Figure()
        
        # Create an axis object
        self.ax = self.figure.add_subplot(1,1,1)

        # Create a layout
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)

        # Create a FigureCanvas
        self.canvas = FigureCanvas(self.figure)
       
        layout = QGridLayout(self._main)
 
        # Add the canvas to the layout
        layout.addWidget(self.canvas,0,0,1,5)
        self.addToolBar(NavigationToolbar(self.canvas, self))
        
        # Create a list of horizontal sliders
        self.sliders = {key:None for key in self.dim_names}
        self.steppers = {key:None for key in self.dim_names}
        self.buttons = []
 
        for dim in self.dims:
        
            # Create a slider for dimension-i
            dim.create_slider(self.slider_change(dim))

            # Create X and Y buttons for the slider
            x_func = self.press_button(dim,0,1)
            y_func = self.press_button(dim,1,0)
            dim.create_buttons(x_func,y_func)

            dim.create_label()

            dim.create_stepper(self.stepper_change(dim))

            # Add the buttons and slider to the box
            layout.addWidget(dim.label, dim.no+1, 0)
            layout.addWidget(dim.buttons[0], dim.no+1, 1)
            layout.addWidget(dim.buttons[1], dim.no+1, 2)
            layout.addWidget(dim.slider, dim.no+1, 3)
            layout.addWidget(dim.stepper, dim.no+1, 4)
       
        self.prepare_initial_view()

    def prepare_initial_view(self):

	# Use the first n - 2 dimensions for the slice viewer
        for i in range(self.n_dims - 2):
            self.slice_selection[self.dim_names[i]] = 0

        # Set the last two dimensions as the x and y axes
        self.axes = [self.dims[-2], self.dims[-1]]

        # Reshape the array for the initial configuration
        arr = self.xarr.isel(self.slice_selection).transpose(self.dim_names[-1],self.dim_names[-2])

        self.axes[0].buttons[0].setChecked(True)
        self.axes[1].buttons[1].setChecked(True)

        for dim in self.axes:

            dim.slider.setVisible(False)
            dim.stepper.setVisible(False)

        # Plot the random array
        self.im = self.ax.imshow(arr)
        self.cbar = self.figure.colorbar(self.im)

        # self.im.autoscale()

        self.ax.set_xlabel(self.axes[0].name)
        self.ax.set_ylabel(self.axes[1].name)

    def press_button(self, dim, curr_axis_no, neighb_axis_no):

        def slice_changer():

           if self.axis_already_selected(dim,curr_axis_no):
               dim.buttons[curr_axis_no].setChecked(False)
               return

           if dim.buttons[curr_axis_no].isChecked():

               # Disable the matching slider and stepper
               dim.slider.setVisible(False)
               dim.stepper.setVisible(False)

               # Switch off the neighbouring button
               dim.buttons[neighb_axis_no].setChecked(False)

               # Set current axis to none
               self.axes[curr_axis_no] = dim
               self.slice_selection.pop(dim.name, None)

               if self.num_buttons_pressed() == 2:
                   print(self.axes)
                   self.change_view()

           else:

               # Enable the matching slider and stepper
               dim.slider.setVisible(True)
               dim.stepper.setVisible(True)

               # Set current axis to current dimension
               self.axes[curr_axis_no] = None
               self.slice_selection[dim.name] = 0

       	   print("Slide selection after button press:")
           print(self.slice_selection)

        return slice_changer

    def axis_already_selected(self,curr_dim,n_curr_axis):

        for dim in self.dims:
            if dim.buttons[n_curr_axis].isChecked() and dim != curr_dim:
                return True
        return False
 
    def stepper_change(self,dim):
   
        # totally clear names 
        def step_changer():


            if self.num_buttons_pressed() == 1:
                dim.slider.setValue(self.slice_selection[dim.name])
                dim.stepper.setValue(self.slice_selection[dim.name])
                return

            print("Step value changed.")
            print("Step value changed.")

            # Obtain the slider value
            stepper_val = dim.stepper.value()
      
            # Change slider value
            dim.slider.setValue(stepper_val)

            # Use value change function 
            self.slider_change(dim)()
 
        return step_changer
        
    def slider_change(self,dim):
   
        # totally clear names 
        def slider_changer():

            if self.num_buttons_pressed() == 1:
                dim.slider.setValue(self.slice_selection[dim.name])
                dim.stepper.setValue(self.slice_selection[dim.name])
                return

            # Obtain the slider value
            slider_val = dim.slider.value()
     
            # Change the stepper value
            dim.stepper.setValue(slider_val)
 
            # Create a dictionary for the  
            self.slice_selection[dim.name] = slider_val

            print("Slide selection:")
            print(self.slice_selection)

            self.change_view() 
 
        return slider_changer
       
    def change_view(self):

        # Create a 2D array
        arr = self.xarr.isel(self.slice_selection).transpose(self.axes[1].name,self.axes[0].name)

        # Plot the reshaped array
        self.im.set_data(arr)
        print(type(self.im)) 
 
        # Label the axes    
        self.ax.set_xlabel(self.axes[0].name)
        self.ax.set_ylabel(self.axes[1].name)

        # Find the minimum and maximum values of the current array 
        min_val = arr.min().values
        max_val = arr.max().values

        # Update the colourbar 
        self.im.set_clim(min_val,max_val)
        self.cbar.draw_all()

        # Draw the canvas 
        self.canvas.draw()
        
    def num_buttons_pressed(self):

        n_buttons_pressed = 0

        for dim in self.dims:
            for i in range(2):
                if dim.buttons[i].isChecked():
                    n_buttons_pressed += 1

        return n_buttons_pressed
 
if __name__ == "__main__":
    qapp = QtWidgets.QApplication(sys.argv)
    app = ApplicationWindow()
    app.show()
    qapp.exec_()
