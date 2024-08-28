import logging

class CustomFormatter(logging.Formatter):

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s | %(levelname)s: %(message)s"
    error_info = "%(asctime)s | %(levelname)s: %(message)s | %(pathname)s : %(lineno)s"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + error_info + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


debug_mode = True

logger = logging.getLogger("osa")
logger.setLevel(logging.DEBUG if debug_mode else logging.INFO)

# create console handler with a higher log level
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(CustomFormatter())
logger.addHandler(console_handler)

# write logging file if working in debug mode
if debug_mode:
    logging.basicConfig(level=logging.DEBUG, filename="app.log",
                        filemode="w", format="%(asctime)s %(levelname)s %(message)s")
