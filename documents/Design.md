# Dataset Viewer Design

Programming Language: Python 3  
Coding Style: PEP8  
Design Pattern: Model View Presenter (Passive View)  
## Sequence Diagrams
### Pressing an X Button
![X Button Press Sequence Diagram](XButtonPress.png)
## UML Diagram
## Development Principles
* Testing must take place alongside development
* Reviewing must take place before code is merged into the master branch
* The reviewer must be someone other than the developer
* Merging can only take place if all tests pass and the reviewer(s) finds the code satisfactory
## Testing and QA
* Use the `unittest` library
* `mock` the View
