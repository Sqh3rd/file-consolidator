from enum import Enum

class Color(Enum):
    _PREFIX = "\033["

    RED = f"{_PREFIX}0;31m"
    GREEN = f"{_PREFIX}0;32m"
    YELLOW = f"{_PREFIX}0;33m"
    BLUE = f"{_PREFIX}0;34m"
    CYAN = f"{_PREFIX}0;36m"

    BOLD_RED = f"{_PREFIX}1;31m"
    BOLD_GREEN = f"{_PREFIX}1;32m"
    BOLD_YELLOW = f"{_PREFIX}1;33m"
    BOLD_BLUE = f"{_PREFIX}1;34m"
    BOLD_CYAN = f"{_PREFIX}1;36m"

    BRIGHT_RED = f"{_PREFIX}0;91m"
    BRIGHT_GREEN = f"{_PREFIX}0;92m"
    BRIGHT_YELLOW = f"{_PREFIX}0;93m"
    BRIGHT_BLUE = f"{_PREFIX}0;94m"
    BRIGHT_CYAN = f"{_PREFIX}0;96m"

    BOLD_BRIGHT_RED = f"{_PREFIX}1;91m"
    BOLD_BRIGHT_GREEN = f"{_PREFIX}1;92m"
    BOLD_BRIGHT_YELLOW = f"{_PREFIX}1;93m"
    BOLD_BRIGHT_BLUE = f"{_PREFIX}1;94m"
    BOLD_BRIGHT_CYAN = f"{_PREFIX}1;96m"

    END = f"{_PREFIX}0m"