import numpy as np
from numpy import resize
import xarray as xr
import hvplot.xarray
import holoviews as hv

import sys
 
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton, QSlider, QHBoxLayout, QGridLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt,  QCoreApplication
 
import sys
import time

import numpy as np

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

        # Create a random 2D array
        self.arr = np.random.rand(3, 8, 12)
        
        # print(self.arr[:,29,3])
        
        # Obtain number of dimensions in the data
        n_dims = len(self.arr.shape)
        
        # Create a figure
        self.figure = Figure()
        
        # Create an axis object
        self.ax = self.figure.add_subplot(1,1,1)
        
        # Plot the random array
        self.im = self.ax.imshow(self.arr[0])
        self.figure.colorbar(self.im)

        # Create a layout
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        # layout = QtWidgets.QVBoxLayout(self._main)

        # Create a FigureCanvas
        self.canvas = FigureCanvas(self.figure)
       
        layout = QGridLayout(self._main)
 
        # Add the canvas to the layout
        layout.addWidget(self.canvas,0,0,1,3)
        self.addToolBar(NavigationToolbar(self.canvas, self))
        
        # Create a list of horizontal sliders
        self.sliders = [None for _ in range(n_dims)]
        
        for i in range(n_dims):
        
            # Create a slider for dimension-i
            self.sliders[i] = self.create_slider(i)

            # Create X and Y buttons for the slider
            x_button, y_button = self.create_buttons(i)

            # Add the buttons and slider to the box
            layout.addWidget(x_button, i+1, 0)
            layout.addWidget(y_button, i+1, 1)
            layout.addWidget(self.sliders[i], i+1, 2)
        
    def create_slider(self, n_dim):
    
        sl = QSlider(Qt.Horizontal)
        sl.valueChanged.connect(self.value_change(n_dim))
      
        # Set slider values
        sl.setMinimum(0)
        sl.setMaximum(self.arr.shape[n_dim] - 1)
        sl.setValue(0)
        
        # Set tick interval
        sl.setTickInterval(1)
            
        # Disable slider by default
        # sl.setEnabled(False)
        
        return sl
    
    def create_buttons(self, n_dim):
   
        # todo - make the buttons do something 
        return [QPushButton("X"), QPushButton("Y")]
    
    def value_change(self,n_dim):
   
        # totally clear names 
        def value_changer():

            # Obtain the slider value
            slider_val = self.slider.value()
      
            # Change plot
            self.ax.imshow(self.arr.take(indices=slider_val,axis=n_dim))
           
            # Will this work? 
            self.canvas.draw()
        
        return value_changer
        
if __name__ == "__main__":
    qapp = QtWidgets.QApplication(sys.argv)
    app = ApplicationWindow()
    app.show()
    qapp.exec_()
