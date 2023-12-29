from dataclasses import dataclass
from typing import List, Optional
from .utilities import convert_enum, validate_semver
from .constants import Visibility, DescriptorType
from .content_topic import ContentCourseTopic

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
    topics: List[ContentCourseTopic]
    type: DescriptorType = DescriptorType.MODULE
    descr: Optional[str] = None
    learning_objectives: Optional[List[str]] = None
    visibility: Optional[Visibility] = Visibility.PUBLIC
    tags: Optional[List[str]] = None

    def __post_init__(self):
        self.visibility = convert_enum(self.visibility, Visibility)
        self.type = convert_enum(self.type, DescriptorType)
        validate_semver(self.version)
        self.topics = [ContentCourseTopic(**topic) for topic in self.topics]

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "descr": self.descr,
            "learning_objectives": self.learning_objectives,
            "version": self.version,
            "visibility": self.visibility.name,
            "tags": self.tags,
            "topics": [item.to_dict() for item in self.content]
        }