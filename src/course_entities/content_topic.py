from dataclasses import dataclass
from typing import Optional, List
from .content_item import ContentItem
from .topic import CourseTopic

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
        self.content_items = [ContentItem(**item) for item in self.content_items]
 
    def to_dict(self):
        return {
            "name": self.name,
            "descr": self.descr,
            "visibility": self.visibility.name,
            "type": self.type.name,
            "content_items": [ci.to_dict() for ci in self.content_items]
        }
