from datasetviewer.stack.interfaces.StackViewInterface import StackViewInterface
from datasetviewer.stack.StackPresenter import StackPresenter
from PyQt5.QtWidgets import QStackedWidget, QWidget, QVBoxLayout, QSpacerItem, QSizePolicy

class StackWidget(QStackedWidget, StackViewInterface):

    def __init__(self, dim_view_factory, parent = None):

        QStackedWidget.__init__(self, parent)

        # Create a StackPresenter and give it a reference to the StackView
        self._presenter = StackPresenter(self, dim_view_factory)

    def create_stack_element(self):

        vbox = QWidget()
        layout = QVBoxLayout()
        vbox.setLayout(layout)
        return self.addWidget(vbox)

    def add_dimension_widget(self, idx, widget):

        layout = self.widget(idx).layout()
        layout.addWidget(widget)

    def change_stack_face(self, idx):
        self.setCurrentIndex(idx)

    def delete_widget(self, idx):
        self.removeWidget(self.widget(idx))

    def get_presenter(self):
        return self._presenter

    def prevent_stretch(self, idx):

        layout = self.widget(idx).layout()
        layout.addItem(QSpacerItem(1, 1, QSizePolicy.Fixed, QSizePolicy.Expanding))
        layout.setSpacing(0)
