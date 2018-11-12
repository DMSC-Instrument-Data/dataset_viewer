import numpy as np
from numpy import resize
import xarray as xr
import hvplot.xarray
import holoviews as hv

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

        # Initialise dimension inforamtion
        self.dim_names = ['A','B','C longername']
        self.dim_sizes = [3,8,12] 
       
        # Obtain number of dimensions in the data
        self.n_dims = 3 
        
        self.dims = [Dimension(self.dim_names[i],self.dim_sizes[i],i) for i in range(self.n_dims)] 

        # Create a random 2D array
        self.arr = np.random.rand(*self.dim_sizes)
      
        self.xarr = xr.DataArray(self.arr, coords = [d.coords for d in self.dims], dims = self.dim_names)
        fig = self.xarr.plot()

        print(type(fig))

        for f in fig:
            print(f)
 
        # Create a figure
        self.figure = Figure()
        
        # Create an axis object
        self.ax = self.figure.add_subplot(1,1,1)
      
        # List for storing the index of the current X/Y axes 
        self.axes = [None, None]
 
        # Plot the random array
        self.im = self.ax.imshow(self.arr[0])
        self.figure.colorbar(self.im)

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
        self.sliders = [None for _ in range(self.n_dims)]
        self.steppers = [None for _ in range(self.n_dims)]
        self.buttons = []
 
        for dim_no in range(self.n_dims):
        
            # Create a slider for dimension-i
            self.sliders[dim_no] = self.create_slider(dim_no)

            # Create X and Y buttons for the slider
            x_button, y_button = self.create_buttons(dim_no)

            button_list = [x_button, y_button]
            self.buttons.append(button_list)            

            dim_label = QLabel()
            dim_label.setText(self.dim_names[dim_no])

            self.steppers[dim_no] = self.create_stepper(dim_no)

            # Add the buttons and slider to the box
            layout.addWidget(dim_label, dim_no+1, 0)
            layout.addWidget(x_button, dim_no+1, 1)
            layout.addWidget(y_button, dim_no+1, 2)
            layout.addWidget(self.sliders[dim_no], dim_no+1, 3)
            layout.addWidget(self.steppers[dim_no], dim_no+1, 4)
        
    def create_slider(self, dim_no):
    
        sl = QSlider(Qt.Horizontal)
        sl.valueChanged.connect(self.slider_change(dim_no))
      
        # Set slider values
        sl.setMinimum(0)
        sl.setMaximum(self.arr.shape[dim_no] - 1)
        sl.setValue(0)
        
        # Set tick interval
        sl.setTickInterval(1)
            
        # Disable slider by default
        # sl.setEnabled(False)
        
        return sl
   
    def create_stepper(self, dim_no):

        stepper = QSpinBox()

        stepper.setRange(0,self.dim_sizes[dim_no]-1)

        stepper.valueChanged.connect(self.stepper_change(dim_no))

        return stepper

    def create_buttons(self, n_curr_dim):
  
        x_button = QPushButton("X")
        x_button.setCheckable(True)
        x_button.clicked.connect(self.press_button(n_curr_dim,0,1))
 
        y_button = QPushButton("Y") 
        y_button.setCheckable(True)
        y_button.clicked.connect(self.press_button(n_curr_dim,1,0))
   
        return [x_button, y_button]

    def press_button(self, n_curr_dim, n_curr_axis, n_neigh_axis):

        def slice_changer():

           if self.other_already_pressed(n_curr_dim,n_curr_axis):
               self.buttons[n_curr_dim][n_curr_axis].setChecked(False)
               return

           if not self.buttons[n_curr_dim][n_curr_axis].isChecked():

               # Enable the matching slider
               self.sliders[n_curr_dim].setVisible(True)

               # Set axes to none
               self.axes[n_curr_axis] = None

           else:
               # Disable the matching slider
               self.sliders[n_curr_dim].setVisible(False)

               # Switch off the neighbouring button
               self.buttons[n_curr_dim][n_neigh_axis].setChecked(False)

               # Set axes to none
               self.axes[n_curr_axis] = n_curr_dim

        return slice_changer

    def other_already_pressed(self,n_curr_dim,n_curr_axis):

        for i in range(self.n_dims):
            if self.buttons[i][n_curr_axis].isChecked() and i != n_curr_dim:
                return True
        return False
 
    def stepper_change(self,n_curr_dim):
   
        # totally clear names 
        def step_changer():

            # Obtain the slider value
            stepper_val = self.steppers[n_curr_dim].value()
      
            # Change slider value
            self.sliders[n_curr_dim].setValue(stepper_val)

            # Use value change function 
            self.slider_change(n_curr_dim)()
 
        return step_changer
        
    def slider_change(self,dim_no):
   
        # totally clear names 
        def slider_changer():

            # Obtain the slider value
            slider_val = self.sliders[dim_no].value()
     
            # Change the stepper value
            self.steppers[dim_no].setValue(slider_val)
 
            # Change plot

            if self.axes == sorted(self.axes):
                self.ax.imshow(self.arr.take(indices=slider_val,axis=dim_no).transpose())
            else:
                self.ax.imshow(self.arr.take(indices=slider_val,axis=dim_no))
            # Will this work? 
            self.canvas.draw()
        
        return slider_changer
        
if __name__ == "__main__":
    qapp = QtWidgets.QApplication(sys.argv)
    app = ApplicationWindow()
    app.show()
    qapp.exec_()
