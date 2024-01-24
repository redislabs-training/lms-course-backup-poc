import requests
import os
import logging
import time
import yaml
from datetime import datetime
from src.course_entities import Course
from .config import WORKSPACE, COURSE_SOURCE, EDX_STUDIO_URL, EDX_LMS_URL, EDX_CLIENT_ID, EDX_CLIENT_SECRET
from .utilities import parse_course_xml, course_package_path, get_api_jwt

def main():
    logging.info('Prepping for course import.')
    course_xml_path = os.path.join(WORKSPACE, 'course.xml')
    course, org = parse_course_xml(course_xml_path)
    package_path = course_package_path(org,course,WORKSPACE)


    # run = datetime.now().strftime("%Y_%-m")
    # # until the version is in the output somewhere I will pull it, would prefer to use course export
    # with open(f'{COURSE_SOURCE}/course.yaml', 'r') as file:
    #     course_data = yaml.safe_load(file)
    # course_obj = Course(**course_data)

    access_token = get_api_jwt(EDX_CLIENT_ID,EDX_CLIENT_SECRET,EDX_LMS_URL)

    pre_provisioned_id = "course-v1:ru+ru001+2024_01"


    task_id = _import_course(pre_provisioned_id, access_token, package_path)
    #task_id = '7d05f243-967b-427f-9f89-a83ee4be4084'

    if task_id:
        logging.info(f"Course import started. Task ID: {task_id}")
        #_poll_import_task(task_id, access_token)



def _import_course(course_id, access_token, package_path):
    """
    Imports a course using the edx rest api

    Args:
    course_id(str): course id to import new content into
    access_token: JWT for edx rest api
    package_path: path to course package
    """

    # Construct the course_id
    # course_id = f"{course_short_name}:{course_org}+{course_version}+{course_run}"


    edx_import_url = f"{EDX_STUDIO_URL}/api/courses/v0/import/{course_id}/"

    files = {'course_data': (os.path.basename(package_path), open(package_path, 'rb'), 'application/gzip')}

    logging.debug(f"calling import url: {edx_import_url}")


    response = requests.post(edx_import_url, files=files, headers={"Authorization": f"JWT {access_token}"})

    if response.status_code == 200:
        logging.debug(response.json())
        return response.json().get('task_id')
    else:
        logging.error(f"Error importing course: {response.text}")
        return None

def _poll_import_task(task_id, access_token, poll_interval=2):
    """
    Polls the task status from OpenEdx API and logs the progress.

    Args:
    task_id (str): ID of the task to poll.
    poll_interval (int): Time interval (in seconds) between each poll. Default is 2 seconds.
    """
    task_url = f"{EDX_STUDIO_URL}/api/tasks/v0/tasks/{task_id}/"
    logging.debug(f"url: {task_url}, token: {access_token}")
    while True:
        response = requests.get(task_url, headers={"Authorization": f"JWT {access_token}", "Accept": "application/json"})

        if response.status_code != 200:
            logging.error(f"Error polling task status: {response.text}")
            break

        data = response.json()
        total_steps = data.get('total_steps', 1)  # Prevent division by zero
        completed_steps = data.get('completed_steps', 0)
        
        percentage_complete = (completed_steps / total_steps) * 100
        logging.info(f"Task {task_id} is {percentage_complete:.2f}% complete")

        if completed_steps >= total_steps:
            logging.info("Task is 100% complete")
            break

        time.sleep(poll_interval)
