import os
import logging
import xml.etree.ElementTree as ET
from ..config import WORKSPACE, ORG, MODULES
from .utilities import normalize_short_name, get_id, current_datetime, future_datetime
from .chapter import gen_chapter, add_sequential_chapter
from .vertical import gen_verticals
from .sequential import gen_sequential

_DIR = f"{WORKSPACE}/course"

def gen_structure(course):
    logging.info('generate course structure')
    _write_course(normalize_short_name(course.short_name), ORG, course.full_name)
    _write_course_structure(course)


def _write_course(short_name, org, full_name):
    course_elem = ET.Element("course", url_name=short_name, org=org, course=full_name)
    filepath = os.path.join(WORKSPACE, "course.xml")
    tree = ET.ElementTree(course_elem)
    tree.write(filepath, encoding="UTF-8", xml_declaration=False)
    logging.info(f'write course.xml at {filepath}')


def _write_course_structure(course):
    filepath = os.path.join(_DIR, f"{normalize_short_name(course.short_name)}.xml")
    modules = [f'&quot;{element}&quot;' for element in MODULES]
    #until we figure it out
    course_elem = ET.Element("course", 
                             advanced_modules=f"[{', '.join(modules)}]",
                             course_image=os.path.basename(course.icon),
                             language="en",
                             display_name=course.full_name,
                             learning_info="[]",
                             instructor_info="{&quot;instructors&quot;: []}",
                             start=current_datetime(),
                             end=future_datetime(60),
                             cert_html_view_enabled="true"
                             )

    for topic in course.topics:
        chapter_id = get_id()
        sequential_id = get_id()
        logging.debug(f"chapter id: {chapter_id}, sequential id: {sequential_id}")

        gen_chapter(chapter_id,topic.name)
        add_sequential_chapter(chapter_id, sequential_id)
        gen_sequential(sequential_id,topic.name)
        gen_verticals(sequential_id,topic.content_items,course)
        ET.SubElement(course_elem, "chapter", attrib={'url_name': chapter_id})
    
    tree = ET.ElementTree(course_elem)
    tree.write(filepath, encoding="UTF-8", xml_declaration=False)
    logging.info(f'write course structure at: {filepath}')

