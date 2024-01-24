import logging
import yaml
from src.course_entities import Course
from .config import COURSE_SOURCE, WORKSPACE
from .workspace import create_workspace
from .serializers import gen_about, gen_info, gen_policies, gen_structure

def main():

    create_workspace(WORKSPACE)

    # Load the course.yaml file
    with open(f'{COURSE_SOURCE}/course.yaml', 'r') as file:
        course_data = yaml.safe_load(file)
    course = Course(**course_data)

    gen_about(course)
    gen_info(course)
    gen_policies(course)
    gen_structure(course)





if __name__ == '__main__':
    main()