from dataclasses import dataclass
from .constants import Visibility, ContentItemType
from typing import List, Optional
from .utilities import convert_enum


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
        self.visibility = convert_enum(self.visibility, Visibility)
        self.type = convert_enum(self.type, ContentItemType)

    def to_dict(self):
        return {
            "name": self.name,
            "tracked": self.tracked,
            "type": self.type.name,
            "ref": self.ref,
            "visibility": self.visibility.name,
            "tags": self.tags
        }