# rescore/logger.py

from datetime import datetime

class Color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'

class Logger:
    def __init__(self, name: str):
        self.name = name

    def _log(self, level: str, message: str, color: str):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{color}[{now}] [{self.name}] [{level}] {message}{Color.RESET}")

    def info(self, message: str):
        self._log("INFO", message, Color.GREEN)

    def warning(self, message: str):
        self._log("WARNING", message, Color.YELLOW)

    def error(self, message: str):
        self._log("ERROR", message, Color.RED)

    def custom(self, message: str, color: str = Color.WHITE):
        self._log("CUSTOM", message, color)

    def print_colored(self, message: str, color: str):
        print(f"{color}{message}{Color.RESET}")

# Usage examples:

# logger = Logger("MyLogger")
# logger.info("This is an info message")
# logger.warning("This is a warning message")
# logger.error("This is an error message")
# logger.custom("This is a custom message", color=Color.MAGENTA)
# logger.print_colored("This is a colored print", color=Color.CYAN)
