
name = "datasetviewer"

def plot(ds):

    from collections import OrderedDict
    from datasetviewer.app.MainWindow import MainWindow
    from datasetviewer.fileloader.FileLoaderTool import dataset_to_dict, invalid_dict
    from PyQt5 import QtWidgets
    import sys
    from xarray.core.dataset import Dataset

    if type(ds) is Dataset:
        ds = dataset_to_dict(ds)

    elif type(ds) is not OrderedDict:
        raise ValueError("Error: Argument is not a Dataset.")

    if invalid_dict(ds):
        raise ValueError("Error: Dataset elements must all have at least one dimension.")

    QAPP = QtWidgets.QApplication(sys.argv)
    APP = MainWindow(script_mode=True, dataset=ds)
    APP.show()
    QAPP.exec_()
