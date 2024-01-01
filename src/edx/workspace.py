import os
import logging
from .config import WORKSPACE


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

    if not os.path.exists(WORKSPACE):
        os.makedirs(WORKSPACE)
    
    logging.debug('create_workspace directories')
    for directory in directories:
        path = os.path.join(WORKSPACE, directory)
        os.makedirs(path, exist_ok=True)