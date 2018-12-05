# Dataset Viewer Design

Programming Language: Python 3.6  
Coding Style: PEP8  
Design Pattern: Model View Presenter (Passive View)

The [MSlice](https://github.com/mantidproject/mslice) tool served as a guideline when designing the Dataset Viewer and informed the choice of design pattern.

## Class Diagram
![Class Diagram](ClassDiagram.png)  
DimensionView: Contains the slider, buttons, and stepper for an individual dimension.  
DimensionPresenter: Manages the behavior of the DimensionView.  
MainView: Contains the individual DimensionViews and the central plot.  
MainPresenter: Manages the behavior of the MainView and retrieves data from the MainModel.  
MainModel: Contains the data array. 
## Sequence Diagrams
These sequence diagrams illustrate the object interactions that occur in the case of the following user actions: 
* Pressing an X button for one of the dimensions
* Changing the stepper value for one of the dimensions
### Pressing an X Button
![X Button Press Sequence Diagram](XButtonPress.png)
### Stepper Change
![Stepper Change Sequence Diagram](StepperChange.png)
## Development Principles
* All programming will follow a test-driven development approach
* At least one reviewer must examine the code and this reviewer cannot be a developer on the project
* All presenters and tests will be created prior to the development of any concrete views
## Testing and QA Principles
* Testing will be done with the `unittest` library
* `mock`s will be created for the the View
* Test coverage will be measured with the aim to achieve a coverage of at least 85%
* All tests will be executed by the CI build server
* Tests should be written to the same quality as the rest of the codebase
* Tests must not be changed without good justification
* Destructive and happy-path tests will be put in place
## Merging Conditions
* All tests pass
* All builds pass
* All reviewers find the code satisfactory
