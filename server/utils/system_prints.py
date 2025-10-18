import sys
from enums import TerminalStyleEnum


class SysPrint:
    SUCCESS = TerminalStyleEnum.GREEN
    ERROR = TerminalStyleEnum.RED
    RESET = TerminalStyleEnum.RESET

    def print_success(self, message: str):
        sys.stdout.write(f"{self.SUCCESS}{message}{self.RESET}\n")
        sys.stdout.flush()

    def print_error(self, message: str):
        sys.stdout.write(f"{self.ERROR}{message}{self.RESET}\n")
        sys.stdout.flush()
