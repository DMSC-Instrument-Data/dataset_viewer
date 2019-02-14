
name = "datasetviewer"

def plot(ds):

    import collections
    from datasetviewer.app.MainWindow import MainWindow
    from PyQt5 import QtWidgets
    import sys

    if type(ds) is not collections.OrderedDict:
        raise ValueError("Error: Argument is not of type Dataset.")

    QAPP = QtWidgets.QApplication(sys.argv)
    APP = MainWindow(script_mode=True, dataset=ds)
    APP.show()
    QAPP.exec_()
