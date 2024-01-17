import os
import logging
from ..config import WORKSPACE
import xml.etree.ElementTree as ET

_DIR = f"{WORKSPACE}/sequential"

def gen_sequential(sequential_id,name):
    file_path = os.path.join(_DIR, f"{sequential_id}.xml")
    chapter_elem = ET.Element("sequential", display_name=name)
    tree = ET.ElementTree(chapter_elem)
    tree.write(file_path, encoding="UTF-8", xml_declaration=False)
    logging.info(f'write new sequential at {file_path}')

def add_vertical_sequential(sequential_id, vertical_id):
    file_path = os.path.join(_DIR, f"{sequential_id}.xml")
    tree = ET.parse(file_path)
    root = tree.getroot()
    if root.tag != 'sequential':
        logging.error(f"The root element of {file_path} is not 'sequential'.")
        return
    vertical_elem = ET.Element("vertical", url_name=vertical_id)
    root.append(vertical_elem)

    tree.write(file_path, encoding="UTF-8", xml_declaration=False)
    logging.info(f'Appended new vertical with id {vertical_id} to sequential at {file_path}')

    