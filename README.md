# Dataset Viewer
[![Build Status](https://travis-ci.org/DMSC-Instrument-Data/dataset_viewer.svg?branch=master)](https://travis-ci.org/DMSC-Instrument-Data/dataset_viewer)
[![Coverage Status](https://coveralls.io/repos/github/DMSC-Instrument-Data/dataset_viewer/badge.svg?branch=master)](https://coveralls.io/github/DMSC-Instrument-Data/dataset_viewer?branch=master)

## Installation

From top directory run
1. `python setup.py install`
2. `start-datasetviewer.py`

## Tests

`python setup.py nosetests`

## Flake8

`python setup.py flake8`

## Issues

* Inconsistent spacing of dimension elements (slider, buttons, etc) 
* Preview pane uses up more space than plot and sliders (Potential solution [here](https://stackoverflow.com/questions/6337589/qlistwidget-adjust-size-to-content))
* Possible to squeeze plot out of existence which creates a `ValueError` for 2D plots and a `UserWarning` for 1D plots
* Default plot may be too small and requires window to be resized