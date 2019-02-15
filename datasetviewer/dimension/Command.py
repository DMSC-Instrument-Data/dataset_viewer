from enum import Enum

class Command(Enum):

    # Indicates that a X button has been checked or unchecked
    XBUTTONCHANGE = 300

    # Indicated than a Y button has been checked or unchecked
    YBUTTONCHANGE = 301

    # Indicates that the slider value has changed
    SLIDERCHANGE = 302

    # Indicates that the stepper value has been changed
    STEPPERCHANGE = 303
