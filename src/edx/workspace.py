import os
import logging
from .config import WORKSPACE
import shutil
import time

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

    if os.path.exists(WORKSPACE):
        backup_dir = f'{WORKSPACE}_{int(time.time())}'
        logging.debug(f'create_workspace WORKSPACE exists, backing up to: {backup_dir}')
        shutil.move(WORKSPACE, backup_dir)
    
    os.makedirs(WORKSPACE)
    
    logging.debug('create_workspace directories')
    for directory in directories:
        path = os.path.join(WORKSPACE, directory)
        os.makedirs(path, exist_ok=True)