import tarfile
import os
import logging
from .config import WORKSPACE
from .utilities import parse_course_xml, course_package_path

def main():
    logging.info(f"packaging course at:{WORKSPACE}")

    _package_course(WORKSPACE)

def _package_course(output_dir):
    course_xml_path = os.path.join(output_dir, 'course.xml')
    course, org = parse_course_xml(course_xml_path)
    package_path = course_package_path(org,course,WORKSPACE)
    
    with tarfile.open(package_path, "w:gz") as tar:

        tar.add(output_dir, arcname=os.path.basename(output_dir))
    
    logging.info(f"Course packaged as {package_path}")