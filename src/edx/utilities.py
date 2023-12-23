import logging

def convert_visibility(visibility, Visibility):
    if isinstance(visibility, str):
        logging.debug("converting visibility str to Visibility enum type")
        visibility = Visibility[visibility]
    if not isinstance(visibility, Visibility):
        raise TypeError("visibility must be an instance of Visibility enum")
    return visibility

def convert_content_item_type(content_type, ContentType):
    if isinstance(content_type, str):
        logging.debug("converting content_type str to ContentType enum type")
        content_type = ContentType[content_type]
    if not isinstance(content_type, ContentType):
        raise TypeError("content_type must be an instance of ContentType enum")
    return content_type

def convert_course_type(course_type, CourseType):
    if isinstance(course_type, str):
        logging.debug("converting course_type str to CourseType enum type")
        course_type = CourseType[course_type]
    if not isinstance(course_type, CourseType):
        raise TypeError("visibility must be an instance of Visibility enum")
    return course_type