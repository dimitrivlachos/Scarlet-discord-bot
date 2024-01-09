import logging

class ColouredFormatter(logging.Formatter):
    DEFAULT_FORMAT = "%(levelname)s: %(message)s"
    LEVEL_COLOURS = {
        logging.DEBUG: "\033[0;36m",   # Cyan for DEBUG
        logging.INFO: "\033[0;32m",    # Green for INFO
        logging.WARNING: "\033[0;33m", # Yellow for WARNING
        logging.ERROR: "\033[0;31m",   # Red for ERROR
        logging.CRITICAL: "\033[1;31m" # Bright Red for CRITICAL
    }
    RESET = "\033[0m"

    def format(self, record):
        colour = getattr(record, 'colour', self.LEVEL_COLOURS.get(record.levelno))
        message = super().format(record)
        return f"{colour}{message}{self.RESET}"

# Logger setup (same as before)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_name = 'bot_event_logs.log'
file_handler = logging.FileHandler(file_name)
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
colour_formatter = ColouredFormatter(ColouredFormatter.DEFAULT_FORMAT)
stream_handler.setFormatter(colour_formatter)
logger.addHandler(stream_handler)

if __name__ == '__main__':
    # Example usage
    logger.debug("Standard debug message")
    logger.info("Standard info message")
    logger.warning("Standard warning message")
    logger.error("Standard error message")
    logger.critical("Standard critical message")
    logger.log(logging.INFO, "Custom coloured message", extra={'colour': "\033[0;35m"})  # Magenta colour
