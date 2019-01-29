from datasetviewer.stack.interfaces.StackViewInterface import StackViewInterface
from PyQt5.QtWidgets import QStackedWidget, QWidget, QHBoxLayout

class StackWidget(QStackedWidget, StackViewInterface):

    def __init__(self, parent = None):

        QStackedWidget.__init__(self, parent)

    def create_stack_element(self):

        hbox = QWidget()
        layout = QHBoxLayout()
        hbox.setLayout(layout)
        return self.addWidget(hbox)

    def add_dimension_view(self, idx, dim_view):

        hbox = self.widget(idx)
        layout = hbox.layout()
        layout.addWidget(dim_view)

    def change_stack_face(self, idx):

        self.setCurrentIndex(idx)

    def delete_widget(self, idx):
        self.removeWidget(self.widget(idx))
