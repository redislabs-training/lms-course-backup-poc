from dataclasses import dataclass
from typing import List, Optional, Union
from .utilities import convert_enum, validate_semver
from .constants import Visibility, DescriptorType, TopicType
from .dependency import Dependency
from .content_topic import ContentCourseTopic
from .module_topic import ModuleCourseTopic

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
        dependencies (Optional[List[Dependency]]): A list of dependencies that the course relies on.

    Methods:
        to_dict: Returns a dictionary representation of the course.
    """

    id: str
    full_name: str
    version: str
    topics: List[Union[ContentCourseTopic, ModuleCourseTopic]]
    type: DescriptorType = DescriptorType.COURSE
    dependencies: Optional[List['Dependency']] = None
    short_name: Optional[str] = None
    learning_objectives: Optional[List[str]] = None 
    description: Optional[str] = None
    icon: Optional[str] = None, 
    tag_filter: Optional[str] = None
    visibility: Visibility = Visibility.PUBLIC

    def __post_init__(self):
        self.visibility = convert_enum(self.visibility, Visibility)
        self.type = convert_enum(self.type, DescriptorType)
        if self.dependencies is not None:
            self.dependencies = [Dependency(**dependency) for dependency in self.dependencies]
        validate_semver(self.version)
        initialized_topics = []
        for topic_data in self.topics:
            if topic_data['type'] == TopicType.CONTENT.value:  # Assuming type is a string "CONTENT" or "MODULE"
                initialized_topics.append(ContentCourseTopic(**topic_data))
            elif topic_data['type'] == TopicType.MODULE.value:
                initialized_topics.append(ModuleCourseTopic(**topic_data))
            else:
                raise ValueError(f"Unknown topic type: {topic_data['type']}")
        self.topics = initialized_topics

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
            "visibility": self.visibility.name,
            "dependencies": [dependency.to_dict() for dependency in self.dependencies]
        }