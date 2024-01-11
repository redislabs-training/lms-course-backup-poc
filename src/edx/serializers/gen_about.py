import os
import logging
from ..config import WORKSPACE
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from src.course_entities import Course

_DIR=f"{WORKSPACE}/about/"

def gen_about(course_data):
    logging.info(f'gen section: {_DIR}')

    course = Course(**course_data)

    _overview_page(course)
    _short_description_page(course)


def _overview_page(course):
    logging.info('gen overview page')

    current_file_dir = Path(__file__).parent
    templates_dir = current_file_dir / "templates"
    env = Environment(loader=FileSystemLoader(str(templates_dir)))
    template = env.get_template('overview.html.j2')


    about_html = f"<p>{course.description}</p><p><strong>Learning Objectives:</strong><ul>"
    about_html += "".join(f"<li>{obj}</li>" for obj in course.learning_objectives)
    about_html += "</ul></p>"

    output_html = template.render(about=about_html)

    os.makedirs(_DIR, exist_ok=True)
    
    with open(os.path.join(_DIR, 'overview.html'), 'w') as file:
        file.write(output_html)

def _short_description_page(course):
    logging.info('gen short_description page')

    os.makedirs(_DIR, exist_ok=True)
    
    with open(os.path.join(_DIR, 'short_description.html'), 'w') as file:
        file.write(course.description)
