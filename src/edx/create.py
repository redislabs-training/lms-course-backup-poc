import logging
import yaml

from .config import COURSE_SOURCE
from .workspace import create_workspace
from .serializers import gen_about, gen_policies

def main():

    create_workspace()

    # Load the course.yaml file
    with open(f'{COURSE_SOURCE}/course.yaml', 'r') as file:
        course_data = yaml.safe_load(file)
    
    gen_about(course_data)
    gen_policies(course_data)

    

if __name__ == '__main__':
    main()