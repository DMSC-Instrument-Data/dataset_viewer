from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton, QSlider, QHBoxLayout
from PyQt5.QtCore import Qt

class SliderGroup(QWidget):

    def __init__(self, n_dim, arr, ax, canvas, parent=None):

        self.arr = arr
        self.ax = ax
        self.canvas = canvas

        QWidget.__init__(self, parent)
        self.setLayout(QHBoxLayout())

        # Create a slider for dimension-i
        self.slider = self.create_slider(n_dim)

        # Create X and Y buttons for the slider
        x_button, y_button = self.create_buttons(n_dim)

        # Add the buttons and slider to the box
        self.layout().addWidget(x_button)
        self.layout().addWidget(y_button)
        self.layout().addWidget(self.slider)

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

