from enum import Enum

class Color(Enum):
    _PREFIX = "\033["
    BRIGHT_RED = _PREFIX + "91m"
    RED = _PREFIX + "31m"
    BRIGHT_BLUE = _PREFIX + "94m"
    BLUE = _PREFIX + "94"
    BRIGHT_YELLOW = _PREFIX + "93m"
    YELLOW = _PREFIX + "33m"
    BRIGHT_CYAN = _PREFIX + "96m"
    CYAN = _PREFIX + "36m"
    END = _PREFIX + "0m"