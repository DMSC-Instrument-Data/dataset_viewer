from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton, QSlider, QHBoxLayout
from PyQt5.QtCore import Qt

class SliderGroup(QWidget):

    def __init__(self, n_dim, arr, ax, canvas, parent=None):

        self.arr = arr
        self.ax = ax
        self.canvas = canvas

        QWidget.__init__(self, parent)
        self.setLayout(QHBoxLayout())



