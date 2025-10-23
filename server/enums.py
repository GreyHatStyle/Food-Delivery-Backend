from enum import Enum


class TerminalStyleEnum(Enum):
    GREEN = "\033[92m"
    RESET = "\033[0m"
    RED = "\033[91m"
    BLUE = "\033[34m"
    BOLD = "\033[1m"

    def __str__(self) -> str:
        return self.value

    # Allow direct use if f-strings and string operations
    __repr__ = __str__
