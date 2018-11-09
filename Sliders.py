import numpy as np
from numpy import resize
import xarray as xr
import hvplot.xarray
import holoviews as hv

import sys
 
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton, QSlider, QHBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt,  QCoreApplication
 
import sys
import time

import numpy as np

import matplotlib.pyplot as plt

from SliderGroup import SliderGroup

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
        layout = QtWidgets.QVBoxLayout(self._main)

        # Create a FigureCanvas
        self.canvas = FigureCanvas(self.figure)
        
        # Add the canvas to the layout
        layout.addWidget(self.canvas)
        self.addToolBar(NavigationToolbar(self.canvas, self))
        
        # Create a list of horizontal sliders
        self.sliders = [None for _ in range(n_dims)]
        
        for i in range(n_dims):
        
            layout.addWidget(SliderGroup(i,self.arr,self.ax,self.canvas))
            
if __name__ == "__main__":
    qapp = QtWidgets.QApplication(sys.argv)
    app = ApplicationWindow()
    app.show()
    qapp.exec_()
