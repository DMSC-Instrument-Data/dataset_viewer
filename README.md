# Python Dataset Viewer Prototype
## Summary
Prototype for viewing slices of n-D datasets.
## Usage

The program uses Python 3.  

Launching the program:
``` python Sliders.py ```

The prototype generates and plots a random 7D array. By default, the final two dimensions are selected as the X and Y axes for the starting view. Changing an axis selection can be done by unchecking one X/Y button and clicking another. Moving through the slices can be done by using the sliders or stepper. The sliders and steppers will not change unless both an X and Y dimension have been selected.

## Known Issues
- Stepper sometimes jumps two values for larger arrays: similar problem and potential solution discussed [here](https://stackoverflow.com/questions/41568990/how-do-i-prevent-double-valuechanged-events-when-i-press-the-arrows-in-a-qspinbo)
- Using ``` self.im.set_clim(min_val,max_val) ``` updates colourbar but doesn't allow plot shape to change
## To-Do
- Implement 1D plots
- ~~Add a way of choosing between a log or linear scale~~
  - Update colourbar when a difference scale has been chosen
- Dictionary view
- Key properties panel
- Loading files
