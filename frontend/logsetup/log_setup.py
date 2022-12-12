import logging
import logging.config
from os import path

# logging configuration
logs_file_path = path.join(
    path.dirname(
        path.abspath(__file__)),
    'log_config_file.cfg')

logging.config.fileConfig(logs_file_path)
