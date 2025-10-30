import sys
from enums import TerminalStyleEnum





def print_green(message: str):
    sys.stdout.write(f"{TerminalStyleEnum.GREEN}{message}{TerminalStyleEnum.RESET}\n")
    sys.stdout.flush()

def print_red( message: str):
    sys.stdout.write(f"{TerminalStyleEnum.RED}{message}{TerminalStyleEnum.RESET}\n")
    sys.stdout.flush()

def print_blue( message: str):
    sys.stdout.write(f"{TerminalStyleEnum.BLUE}{message}{TerminalStyleEnum.RESET}\n")
    sys.stdout.flush()
