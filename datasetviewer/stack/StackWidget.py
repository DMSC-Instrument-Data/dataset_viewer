from datasetviewer.stack.interfaces.StackViewInterface import StackViewInterface
from datasetviewer.stack.StackPresenter import StackPresenter
from PyQt5.QtWidgets import QStackedWidget, QWidget, QVBoxLayout

class StackWidget(QStackedWidget, StackViewInterface):

    def __init__(self, dim_fact, parent = None):

        QStackedWidget.__init__(self, parent)

        self._presenter = StackPresenter(self, dim_fact)

    def create_stack_element(self):

        hbox = QWidget()
        layout = QVBoxLayout()
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

    def get_presenter(self):
        return self._presenter
