import os
import logging
from ..config import WORKSPACE
import xml.etree.ElementTree as ET

_DIR = f"{WORKSPACE}/chapter"

def gen_chapter(chapter_id,name):
    file_path = os.path.join(_DIR, f"{chapter_id}.xml")
    chapter_elem = ET.Element("chapter", display_name=name)
    tree = ET.ElementTree(chapter_elem)
    tree.write(file_path, encoding="UTF-8", xml_declaration=False)
    logging.info(f'write new chapter at {file_path}')

def add_sequential_chapter(chapter_id, sequential_id):
    file_path = os.path.join(_DIR, f"{chapter_id}.xml")
    tree = ET.parse(file_path)
    root = tree.getroot()
    if root.tag != 'chapter':
        logging.error(f"The root element of {file_path} is not 'chapter'.")
        return
    sequential_elem = ET.Element("sequential", url_name=sequential_id)
    root.append(sequential_elem)

    tree.write(file_path, encoding="UTF-8", xml_declaration=False)
    logging.info(f'Appended new sequential with id {sequential_id} to chapter at {file_path}')