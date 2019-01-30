from datasetviewer.stack.interfaces.StackViewInterface import StackViewInterface
from datasetviewer.stack.StackPresenter import StackPresenter
from PyQt5.QtWidgets import QStackedWidget, QWidget, QGridLayout

class StackWidget(QStackedWidget, StackViewInterface):

    def __init__(self, dim_fact, parent = None):

        QStackedWidget.__init__(self, parent)

        self._presenter = StackPresenter(self, dim_fact)

        self.setMinimumHeight(300)

    def create_stack_element(self):

        grid = QWidget()
        layout = QGridLayout()
        grid.setLayout(layout)
        return self.addWidget(grid)

    def add_dimension_widget(self, idx, x, y, widget):

        layout = self.widget(idx).layout()
        layout.addWidget(widget, x, y)

    def change_stack_face(self, idx):
        self.setCurrentIndex(idx)

    def delete_widget(self, idx):
        self.removeWidget(self.widget(idx))

    def get_presenter(self):
        return self._presenter
