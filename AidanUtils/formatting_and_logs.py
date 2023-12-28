import logging

# ANSI escape codes for colors and styles
GREEN = '\033[92m'
RED = '\033[91m'  # Red color for errors
BLUE = '\033[94m'  # Blue color for info
BOLD = '\033[1m'
RESET = '\033[0m'  # Resets the style to default


def green_bold_print(message):
    print(f"{GREEN}{BOLD}{message}{RESET}")


def blue_bold_print(message):
    print(f"{BLUE}{BOLD}{message}{RESET}")


# Custom formatter to add escape codes based on log level
class CustomFormatter(logging.Formatter):
    def format(self, record):
        color = GREEN if record.levelno < logging.WARNING else RED
        original = logging.Formatter.format(self, record)
        return f"{color}{BOLD}{original}{RESET}"
