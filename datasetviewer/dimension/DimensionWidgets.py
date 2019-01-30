from datasetviewer.dimension.interfaces.DimensionViewInterface import DimensionViewInterface
from datasetviewer.dimension.DimensionPresenter import DimensionPresenter
from datasetviewer.dimension.Command import Command
from PyQt5.QtWidgets import QLabel, QPushButton, QSlider, QSpinBox
from PyQt5.QtCore import Qt

class DimensionWidgets(DimensionViewInterface):

    def __init__(self, dim_name, dim_size):

        self.dim_name = dim_name
        self.dim_size = dim_size

        self._presenter = DimensionPresenter(self, dim_name)

        self.label = QLabel()
        self.label.setText(dim_name)

        self.x_button = QPushButton("X")
        self.y_button = QPushButton("Y")

        self.slider = QSlider(Qt.Horizontal)
        self.stepper = QSpinBox()

        # Initialise buttons
        self.x_button.setCheckable(True)
        self.y_button.setCheckable(True)

        # Initialise slider
        self.slider.setMinimum(0)
        self.slider.setMaximum(dim_size - 1)
        self.slider.setValue(0)
        self.slider.setTickInterval(1)

        # Initialise stepper
        self.stepper.setRange(0, dim_size - 1)

        # Set up signals
        self.x_button.clicked.connect(lambda: self._presenter.notify(Command.XBUTTONCHANGE))
        self.y_button.clicked.connect(lambda: self._presenter.notify(Command.YBUTTONCHANGE))
        self.slider.sliderMoved.connect(lambda: self._presenter.notify(Command.SLIDERCHANGE))
        self.stepper.valueChanged.connect(lambda: self._presenter.notify(Command.STEPPERCHANGE))

    def get_x_state(self):
        return self.x_button.isChecked()

    def set_x_state(self, state):
        self.x_button.setChecked(state)

    def get_y_state(self):
        return self.y_button.isChecked()

    def set_y_state(self, state):
        self.y_button.setChecked(state)

    def get_slider_value(self):
        return self.slider.value()

    def set_slider_value(self, val):
        self.slider.setValue(val)

    def get_stepper_value(self):
        return self.stepper.value()

    def set_stepper_value(self, val):
        self.stepper.setValue(val)

    def get_presenter(self):
        return self._presenter

    def enable_slider(self):
        self.slider.show()

    def enable_stepper(self):
        self.stepper.show()

    def disable_slider(self):
        self.slider.hide()

    def disable_stepper(self):
        self.stepper.hide()

    def get_widgets(self):
        return [self.label, self.x_button, self.y_button, self.slider, self.stepper]

    def block_signal(self, bool):

        self.slider.blockSignals(bool)
        self.stepper.blockSignals(bool)
