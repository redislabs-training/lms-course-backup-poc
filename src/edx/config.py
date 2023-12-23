import os
import logging

def load_env_variables(env_file=".env"):
    with open(env_file, "r") as file:
        for line in file:
            key, value = line.strip().split('=', 1)
            os.environ[key] = value

load_env_variables()

COURSE_SOURCE = os.getenv("COURSE_SOURCE")
EDX_WORKSPACE = os.getenv("EDX_WORKSPACE")

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

SEMVER_REGEX = r"^v?(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$"