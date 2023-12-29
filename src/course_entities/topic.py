from dataclasses import dataclass
from typing import Optional
from .utilities import convert_enum
from .constants import Visibility, TopicType


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
    visibility: Optional[Visibility] = Visibility.PUBLIC
    type: TopicType = TopicType.CONTENT

    def __post_init__(self):
        self.visibility = convert_enum(self.visibility, Visibility)
        self.type = convert_enum(self.type, TopicType)
