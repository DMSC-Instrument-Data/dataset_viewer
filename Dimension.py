from PyQt5.QtWidgets import QPushButton, QSlider, QLabel, QSpinBox
from PyQt5.QtCore import Qt

class Dimension:

    def __init__(self,name,size,dim_num):

        self.name = name
        self.label = None 
        self.size = size
        self.no = dim_num
        self.slider = None
        self.buttons = [None, None]
        self.stepper = None

    def create_slider(self,change_func):   
 
        self.slider = QSlider(Qt.Horizontal)
        self.slider.valueChanged.connect(change_func)
      
        # Set slider values
        self.slider.setMinimum(0)
        self.slider.setMaximum(self.size - 1)
        self.slider.setValue(0)
        
        # Set tick interval
        self.slider.setTickInterval(1)
            
    def create_buttons(self,x_func,y_func):
  
        x_button = QPushButton("X")
        x_button.setCheckable(True)
        x_button.clicked.connect(x_func)
 
        y_button = QPushButton("Y") 
        y_button.setCheckable(True)
        y_button.clicked.connect(y_func)
   
        self.buttons = [x_button, y_button]

    def create_label(self):

        self.label = QLabel()
        self.label.setText(self.name)

    def create_stepper(self,change_func):

        self.stepper = QSpinBox()

        self.stepper.setRange(0,self.size-1)
        self.stepper.valueChanged.connect(change_func)


