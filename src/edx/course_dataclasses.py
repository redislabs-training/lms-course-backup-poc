import logging
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Union
from .utilities import convert_content_item_type, convert_visibility, convert_course_type, convert_topic_type, validate_semver, initialize_topics

class Visibility(Enum):
    INTERNAL = "INTERNAL"
    TRUSTED = "TRUSTED"
    PUBLIC = "PUBLIC"

class ContentItemType(Enum):
    VIDEO = "VIDEO"
    SLIDES = "SLIDES"
    ARTICLE = "ARTICLE"
    LABEL = "LABEL"
    EXERCISE = "EXERCISE"
    QUIZ = "QUIZ"
    LINK = "LINK"
    ATTMT = "ATTMT"

class TopicType(Enum):
    MODULE = "MODULE"
    CONTENT = "CONTENT"

class CourseType(Enum):
    COURSE = "COURSE"

@dataclass
class Dependency:
    """
    Base class for different types of course topics.

    Attributes:
        name (str): The name of the topic.
        descr (Optional[str]): A description of the topic.
        visibility (Visibility): The visibility status of the topic (INTERNAL, TRUSTED, PUBLIC).
    """
    id: str
    repo: str
    version: str

    def to_dict(self):
        return {
            "id": self.id,
            "repo": self.repo,
            "version": self.version
        }

@dataclass
class ContentItem:
    """
    Represents an item of content in a course.

    Attributes:
        name (str): The name of the content item.
        tracked (bool): Indicates if the content item should be tracked for completion.
        type (ContentItemType): The type of content (e.g., VIDEO, ARTICLE).
        ref (str): A reference to the content item's source or location.
        visibility (Visibility): The visibility status of the content item (INTERNAL, TRUSTED, PUBLIC).
        tags (List[str]): A list of tags associated with the content item.

    Methods:
        to_dict: Returns a dictionary representation of the content item.
    """

    name: str
    type: ContentItemType
    ref: str
    tracked: bool = True
    visibility: Visibility = Visibility.PUBLIC
    tags: Optional[List[str]] = None

    def __post_init__(self):
        self.visibility = convert_visibility(self.visibility, Visibility)
        self.type = convert_content_item_type(self.type, ContentItemType)

    def to_dict(self):
        return {
            "name": self.name,
            "tracked": self.tracked,
            "type": self.type.name,  # Convert enum to string
            "ref": self.ref,
            "visibility": self.visibility.name,  # Convert enum to string
            "tags": self.tags
        }

@dataclass
class CourseModule:
    """
    Represents a module within a course, containing educational content or topics.

    Attributes:
        id (str): Unique identifier for the module.
        name (str): The name of the module.
        descr (Optional[str]): A detailed description of the module.
        learning_objectives (Optional[List[str]]): A list of textual learning objectives.
        version (str): The version of the module.
        visibility (Visibility): The visibility status of the module (INTERNAL, TRUSTED, PUBLIC).
        tags (Optional[List[str]]): A list of tags associated with the module.
        content (Union[List[ContentItem], List[ContentCourseTopic]]): The content of the module, either as direct content items or as topics containing content items.

    Methods:
        to_dict: Returns a dictionary representation of the module.
    """

    id: str
    name: str
    version: str
    topics: List['ContentCourseTopic']
    descr: Optional[str] = None
    learning_objectives: Optional[List[str]] = None
    visibility: Visibility = Visibility.PUBLIC
    tags: Optional[List[str]] = None

    def __post_init__(self):
        self.visibility = convert_visibility(self.visibility, Visibility)
        validate_semver(self.version)
        self.topics = initialize_topics(self.topics, ContentCourseTopic, ModuleCourseTopic, TopicType)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "descr": self.descr,
            "learning_objectives": self.learning_objectives,
            "version": self.version,
            "visibility": self.visibility.name,  # Convert enum to string
            "tags": self.tags,
            "topics": [item.to_dict() for item in self.content]  # Assuming all content has a to_dict method
        }

@dataclass
class CourseTopic:
    """
    Base class for different types of course topics.

    Attributes:
        name (str): The name of the topic.
        descr (Optional[str]): A description of the topic.
        visibility (Visibility): The visibility status of the topic (INTERNAL, TRUSTED, PUBLIC).
    """
    name: str
    descr: Optional[str] = None
    visibility: Visibility = Visibility.PUBLIC
    type: TopicType = TopicType.CONTENT

    def __post_init__(self):
        self.visibility = convert_visibility(self.visibility, Visibility)
        self.type = convert_topic_type(self.type, TopicType)

@dataclass
class ContentCourseTopic(CourseTopic):
    """
    Represents a course topic that contains a list of content items.

    Attributes:
        content_items (List[ContentItem]): A list of content items associated with the topic.
    """
    learning_objectives: Optional[List[str]] = None 
    content_items: List['ContentItem'] = None

    def __post_init__(self):
        # Convert content item dictionaries to ContentItem objects
        self.content_items = [ContentItem(**item) for item in self.content_items]
 

    def to_dict(self):
        return {
            "name": self.name,
            "descr": self.descr,
            "visibility": self.visibility.name,  # Convert enum to string
            "type": self.type.name,
            "content_items": [ci.to_dict() for ci in self.content_items]  # Assuming ContentItem has a to_dict method
        }

@dataclass
class ModuleCourseTopic(CourseTopic):
    """
    Represents a course topic that is linked to a specific module.

    Attributes:
        module (CourseModule): The module associated with the topic.
    """
    module: CourseModule = None

    def to_dict(self):
        return {
            "name": self.name,
            "descr": self.descr,
            "visibility": self.visibility.name,  # Convert enum to string
            "type": self.type.name,
            "module": self.module.to_dict()  # Assuming CourseModule has a to_dict method
        }


@dataclass
class Course:
    """
    Represents a course with various attributes, topics, and dependencies.

    Attributes:
        id (str): Unique identifier for the course.
        full_name (str): The full name of the course.
        short_name (Optional[str]): A shortened name or abbreviation of the course.
        learning_objectives (Optional[List[str]]): A list of textual learning objectives.
        description (Optional[str]): A detailed description of the course.
        version (str): The version of the course.
        icon (Optional[str]): A reference to the course's icon image or graphic.
        topics (List[CourseTopic]): A list of topics associated with the course.
        tag_filter (Optional[str]): A tag used for filtering or categorization.
        visibility (Visibility): The visibility status of the course (INTERNAL, TRUSTED, PUBLIC).
        dependencies (List[Dependency]): A list of dependencies that the course relies on.

    Methods:
        to_dict: Returns a dictionary representation of the course.
    """

    id: str
    full_name: str
    version: str
    dependencies: List['Dependency']
    topics: List[Union[ContentCourseTopic, ModuleCourseTopic]]
    type: CourseType = CourseType.COURSE
    short_name: Optional[str] = None
    learning_objectives: Optional[List[str]] = None 
    description: Optional[str] = None
    icon: Optional[str] = None, 
    tag_filter: Optional[str] = None
    visibility: Visibility = Visibility.PUBLIC

    def __post_init__(self):
        self.visibility = convert_visibility(self.visibility, Visibility)
        self.type = convert_course_type(self.type, CourseType)
        self.dependencies = [Dependency(**dependency) for dependency in self.dependencies]
        validate_semver(self.version)
        self.topics = initialize_topics(self.topics, ContentCourseTopic, ModuleCourseTopic, TopicType)

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type.name,
            "full_name": self.full_name,
            "short_name": self.short_name,
            "learning_objectives": self.learning_objectives,
            "description": self.description,
            "version": self.version,
            "icon": self.icon,
            "topics": [topic.to_dict() for topic in self.topics],
            "tag_filter": self.tag_filter,
            "visibility": self.visibility.name,  # Convert enum to string
            "dependencies": [dependency.to_dict() for dependency in self.dependencies]  # Assuming Dependency has a to_dict method
        }