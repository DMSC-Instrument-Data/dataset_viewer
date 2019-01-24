from enum import Enum

class Command(Enum):

    # Indicates that a X button has been checked or unchecked
    XBUTTONPRESS = 300

    # Indicated than a Y button has been checked or unchecked
    YBUTTONPRESS = 301

    # Indicates that the slider value has changed
    SLIDERCHANGE = 302
