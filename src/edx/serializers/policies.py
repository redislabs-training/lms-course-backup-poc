import os
import logging
from ..config import WORKSPACE, COURSE_SOURCE, ORG, MODULES
from pathlib import Path
import json
import shutil
from dataclasses import asdict
from .utilities import get_mime_type, normalize_short_name
from .assets import add_asset
from .entities import ContentSon, Asset, Policy, GradingPolicy, Tab, UserPartition, Group

_DIR=f"{WORKSPACE}/policies/"

def gen_policies(course):
    logging.info(f'gen section: {_DIR}')

    name = normalize_short_name(course.short_name)
    course_path = os.path.join(_DIR, name)
    os.makedirs(course_path, exist_ok=True)
    if course.icon is not None:
        logo_filename = os.path.basename(course.icon)
        shutil.copy(f'{COURSE_SOURCE}/{course.icon}', f'{WORKSPACE}/static/')
        _add_course_logo(course, name, logo_filename)
    _gen_policy(name, logo_filename, course.full_name)
    _gen_grading_policy(name)

def _add_course_logo(course,name,logo_filename):
    son = ContentSon(name=logo_filename,course=name,org=ORG)
    logo_obj = {'contentType':get_mime_type(course.icon),
        'displayname': logo_filename,
        'filename': f'asset-v1:edu+{course.version}+{name}+type@asset+block@{logo_filename}',
        'content_son': son,
        'thumbnail_location': ["c4x","edu",course.version,"thumbnail",logo_filename,None]
        }
    logo = Asset(**logo_obj)
    add_asset(logo)

def _gen_policy(name, logo_filename, course_full_name):
    logging.info(f'gen policy json file')

    policy = Policy(display_name=course_full_name,course_image=logo_filename)

    policy_obj = {f"course/{name}":asdict(policy)}

    file_path = f'{_DIR}/{name}/policy.json'
    with open(file_path, 'w') as file:
        json.dump(policy_obj, file, indent=4)

def _gen_grading_policy(name):
    logging.info(f'gen grading policy json file')

    grading_policy = GradingPolicy()

    policy_obj = asdict(grading_policy)

    file_path = f'{_DIR}/{name}/grading_policy.json'
    with open(file_path, 'w') as file:
        json.dump(policy_obj, file, indent=4)