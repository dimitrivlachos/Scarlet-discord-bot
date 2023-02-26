'''
This module is used to create a logger object with a file handler.
'''

import logging

# Create a logger object with a file handler
logger = logging.getLogger(__name__)
# Set the logger level to DEBUG
logger.setLevel(logging.DEBUG)

# Create a file handler and set its level and format
file_name = 'bot_event_logs.log'
file_handler = logging.FileHandler(file_name)
file_handler.setLevel(logging.DEBUG)
# Create a formatter and set the formatter for the handler.
# The formatter will add a timestamp to the log message and format it like this:
# 2021-01-01 00:00:00,000 DEBUG This is a log message
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Create a stream handler and set its level and format
# This will print log messages to the console
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(levelname)s: %(message)s')
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)