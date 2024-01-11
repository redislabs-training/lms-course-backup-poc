import os
import logging

def load_env_variables(env_file=".env"):
    with open(env_file, "r") as file:
        for line in file:
            key, value = line.strip().split('=', 1)
            os.environ[key] = value

load_env_variables()

COURSE_SOURCE = os.getenv("COURSE_SOURCE")
WORKSPACE = os.getenv("WORKSPACE")

set_level = os.getenv("LOG_LEVEL")
match set_level:
    case 'DEBUG':
        LOG_LEVEL = logging.DEBUG
    case 'WARNING':
        LOG_LEVEL = logging.WARNING
    case 'ERROR':
        LOG_LEVEL = logging.ERROR
    case 'CRITICAL':
        LOG_LEVEL = logging.CRITICAL
    case _:
        LOG_LEVEL = logging.INFO

logging.basicConfig(
    level=LOG_LEVEL,
    format='%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s'
)