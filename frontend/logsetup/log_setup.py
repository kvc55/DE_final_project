import os
from os import path

import logging
import logging.config

# Import ENV variables.
from dotenv import load_dotenv, find_dotenv
load_dotenv (find_dotenv('../config/.env'))

logging.config.fileConfig(f'{os.getenv("ROOT_PATH")}/logs/log_config_file.cfg')
