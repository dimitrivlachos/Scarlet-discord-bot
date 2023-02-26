'''
This module is used to create a logger object with a file handler.
'''

import logging

file_name = 'bot_event_logs.log'

# Create a logger object with a file handler
logger = logging.getLogger(__name__)
# Set the logger level to DEBUG
logger.setLevel(logging.DEBUG)
# Set the logger level to DEBUG
handler = logging.FileHandler(file_name)
handler.setLevel(logging.DEBUG)

# Create a formatter and set the formatter for the handler.
# The formatter will add a timestamp to the log message and format it like this:
# 2021-01-01 00:00:00,000 DEBUG This is a log message
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
# Set the formatter for the handler
handler.setFormatter(formatter)
# Add the handler to the logger
logger.addHandler(handler)