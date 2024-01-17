import os
import logging
from ..config import WORKSPACE
from pathlib import Path
from .entities import Overview

_DIR=f"{WORKSPACE}/about/"

def gen_about(course):
    logging.info(f'gen section: {_DIR}')

    _overview_page(course)
    _short_description_page(course)


def _overview_page(course):
    logging.info('gen overview page')

    about_html = f"<p>{course.description}</p><p><strong>Learning Objectives:</strong><ul>"
    about_html += "".join(f"<li>{obj}</li>" for obj in course.learning_objectives)
    about_html += "</ul></p>"

    overview = Overview(
        about=about_html,
        prerequisites="",
        staff="",
        faq=""
    )

    with open(os.path.join(_DIR, 'overview.html'), 'w') as file:
        file.write('<section class="about">\n')
        file.write(f'    {overview.about}\n')
        file.write('</section>\n')
        file.write('<section class="prerequisites">\n')
        file.write(f'    {overview.prerequisites or ""}\n')
        file.write('</section>\n')
        file.write('<section class="course-staff">\n')
        file.write(f'    {overview.staff or ""}\n')
        file.write('</section>\n')
        file.write('<section class="faq">\n')
        file.write(f'    {overview.faq or ""}\n')
        file.write('</section>\n')

def _short_description_page(course):
    logging.info('gen short_description page')

    os.makedirs(_DIR, exist_ok=True)
    
    with open(os.path.join(_DIR, 'short_description.html'), 'w') as file:
        file.write(course.description)
