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

# EDX values
ORG = os.getenv("EDX_ORG", "ru")
# comma separate list of modules in a string
MODULES = "[\"pdf\"]"

# set local edx values
EDX_STUDIO_URL = os.getenv("EDX_STUDIO_URL", "http://studio.local.edly.io")
EDX_LMS_URL = os.getenv("EDX_LMS_URL", "http://local.edly.io")
EDX_CLIENT_ID = os.getenv("EDX_CLIENT_ID", "NFQrmeVTPfL3xviTWbRRRA2QWgBMJWTJfIbw3GpY")
EDX_CLIENT_SECRET = os.getenv("EDX_CLIENT_SECRET", "tk8MyEZ64dbp1LZrX4V0MB7IrQ35OGjMjtX98rGOdvpBItuvRAI8IrhxvDOguKq2oBMjeMdDac2oslYwmaNzeiZDVgobm0SqCGMNYWnjXQDlFWC4fwOpOWFAAS3okoI5")