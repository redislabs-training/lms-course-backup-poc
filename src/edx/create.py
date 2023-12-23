import logging
import yaml



from .config import LOG_LEVEL,EDX_WORKSPACE,COURSE_SOURCE
from .workspace import create_workspace

def main():
    
    logging.basicConfig(level=LOG_LEVEL)

    create_workspace()

    # Load the course.yaml file
    with open(f'{COURSE_SOURCE}/course.yaml', 'r') as file:
        course_data = yaml.safe_load(file)

    logging.debug(course_data)

if __name__ == '__main__':
    main()