import logging
import re
from .config import SEMVER_REGEX

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
        raise TypeError("course_type must be an instance of CourseType enum")
    return course_type


def convert_topic_type(topic_type, TopicType):
    if isinstance(topic_type, str):
        logging.debug("converting course_type str to CourseType enum type")
        topic_type= TopicType[topic_type]
    if not isinstance(topic_type, TopicType):
        raise TypeError("topic_type must be an instance of TopicType enum")
    return topic_type


def validate_semver(version: str):
    if not re.match(SEMVER_REGEX, version):
        raise ValueError(f"{version} is not a valid Semantic Version with 'v' prefix")

def initialize_topics(topics, ContentCourseTopic, ModuleCourseTopic, TopicType):
    initialized_topics = []
    for topic_data in topics:
        if topic_data['type'] == TopicType.CONTENT.value:  # Assuming type is a string "CONTENT" or "MODULE"
            initialized_topics.append(ContentCourseTopic(**topic_data))
        elif topic_data['type'] == TopicType.MODULE.value:
            initialized_topics.append(ModuleCourseTopic(**topic_data))
        else:
            raise ValueError(f"Unknown topic type: {topic_data['type']}")
    return initialized_topics