import os
import logging
from .config import EDX_WORKSPACE


def create_workspace():
    logging.debug('create_workspace')
    directories = [
        "about",
        "assets",
        "chapter",
        "html",
        "info",
        "policies",
        "problem",
        "sequential",
        "static",
        "vertical"
    ]

    if not os.path.exists(EDX_WORKSPACE):
        os.makedirs(EDX_WORKSPACE)
    
    logging.debug('create_workspace directories')
    for directory in directories:
        path = os.path.join(EDX_WORKSPACE, directory)
        os.makedirs(path, exist_ok=True)