import os
import logging
from ..config import WORKSPACE
from pathlib import Path
from .entities import Overview

_DIR=f"{WORKSPACE}/info/"

# we don't use these pages right now

def gen_info(course):
    logging.debug(f"info pages for {course.short_name}")

    _handouts_page()
    _updates_page()


def _handouts_page():
    logging.info('gen handouts page')

    os.makedirs(_DIR, exist_ok=True)
    
    with open(os.path.join(_DIR, 'handouts.html'), 'w') as file:
        file.write('<ol></ol>')

def _updates_page():
    logging.info('gen updates page')

    os.makedirs(_DIR, exist_ok=True)
    
    with open(os.path.join(_DIR, 'updates.html'), 'w') as file:
        file.write('<ol></ol>')