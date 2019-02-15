
name = "datasetviewer"

def plot(ds):

    import collections
    from datasetviewer.app.MainWindow import MainWindow
    from datasetviewer.fileloader.FileLoaderTool import dataset_to_dict, invalid_dict
    from PyQt5 import QtWidgets
    import sys
    import xarray

    if type(ds) is xarray.core.dataset.Dataset:
        ds = dataset_to_dict(ds)

    elif type(ds) is not collections.OrderedDict:
        raise ValueError("Error: Argument is not a Dataset.")

    if invalid_dict(ds):
        raise ValueError("Error: Dataset elements must all have at least one dimension.")

    QAPP = QtWidgets.QApplication(sys.argv)
    APP = MainWindow(script_mode=True, dataset=ds)
    APP.show()
    QAPP.exec_()
