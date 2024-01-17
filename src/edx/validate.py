
import logging
from .config import WORKSPACE
from olxcleaner import validate
from olxcleaner.reporting import report_errors
from olxcleaner.loader.xml_exceptions import CourseXMLDoesNotExist

def main():
    
    course, errorstore, urls = validate(WORKSPACE, steps=8, ignore=None, allowed_xblocks=['pdf'])

    if len(errorstore.errors) > 0 and isinstance(errorstore.errors[0], CourseXMLDoesNotExist):
        logging.error(f"{errorstore.errors[0].description}")

    error_report = report_errors(errorstore)

    if errorstore.return_error(3) is True:
        if error_report:
            for line in error_report:
                logging.error(line)
    else:
        logging.info("No validation errors found.")
        #logging.info("Warnings found during validation:")
        # if error_report:
        #     for line in error_report:
        #         logging.info(line)

    #logging.info(urls)
    #logging.info(course)

if __name__ == '__main__':
    main()