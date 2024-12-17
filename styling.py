GREEN = '\033[92m'
YELLOW = '\033[33m'
RED = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
CLS = '\033[2J\033[H'

def colorize(message: str, color: str) -> str:
    """Colorize a message with a given color."""
    return f'{color}{message}{ENDC}'

def bold(message: str) -> str:
    """Bold a message."""
    return f'{BOLD}{message}{ENDC}'

def green(message: str) -> str:
    """Colorize a message in green."""
    return colorize(message, GREEN)

def red(message: str) -> str:
    """Colorize a message in red."""
    return colorize(message, RED)

def yellow(message: str) -> str:
    """Colorize a message in yellow."""
    return colorize(message, YELLOW)

