from PyQt5.QtWidgets import QPushButton, QSlider, QLabel, QSpinBox
from PyQt5.QtCore import Qt

class Dimension:

    def __init__(self,name,size,dim_num):

        self.name = name
        self.size = size
        self.no = dim_num

        self.label = QLabel()
        self.label.setText(self.name)

        self.buttons = [QPushButton("X"), QPushButton("Y")]
        self.slider = QSlider(Qt.Horizontal)
        self.stepper = QSpinBox()

    def prepare_slider(self,change_funcs):

        for change_function in change_funcs:
            self.slider.valueChanged.connect(change_function)

        # Set slider values
        self.slider.setMinimum(0)
        self.slider.setMaximum(self.size - 1)
        self.slider.setValue(0)

        # Set tick interval
        self.slider.setTickInterval(1)

    def prepare_buttons(self,x_func,y_func):

        self.buttons[0].setCheckable(True)
        self.buttons[0].clicked.connect(x_func)

        self.buttons[1].setCheckable(True)
        self.buttons[1].clicked.connect(y_func)

    def prepare_stepper(self,change_funcs):

        self.stepper.setRange(0,self.size-1)

        for change_function in change_funcs:
            self.stepper.valueChanged.connect(change_function)


