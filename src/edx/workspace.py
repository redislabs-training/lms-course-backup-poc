import os
import logging
import shutil
import time

def create_workspace(WORKSPACE):
    logging.debug('setting up WORKSPACE')
    directories = [
        "about",
        "assets",
        "chapter",
        "course",
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
        logging.debug(f'WORKSPACE already exists, backing up to: {backup_dir}')
        shutil.move(WORKSPACE, backup_dir)
    
    os.makedirs(WORKSPACE)
    
    logging.debug('create sub directories')
    for directory in directories:
        path = os.path.join(WORKSPACE, directory)
        os.makedirs(path, exist_ok=True)