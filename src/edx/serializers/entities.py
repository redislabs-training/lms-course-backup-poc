import json
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict
from .utilities import current_datetime


def complex_encoder(obj):
    if isinstance(obj, Policy):
        # Convert each field to a dictionary, recursively
        return {k: complex_encoder(getattr(obj, k)) for k in obj.__dataclass_fields__}
    elif isinstance(obj, (Tab, UserPartition, Group)):
        return obj.__dict__
    return obj


@dataclass
class Tab:
    name: str
    type: str
    course_staff_only: bool = False
    is_hidden: Optional[bool] = None
    url_slug: Optional[str] = None

@dataclass
class Group:
    id: int
    name: str
    version: int

@dataclass
class UserPartition:
    active: bool
    description: str
    groups: List[Group]

@dataclass
class Policy:
    course_logo: Optional[str]
    start: Optional[str] = field(default_factory=current_datetime)
    show_calculator: bool = False
    show_reset_button: bool = False
    advanced_modules: List[str] = field(default_factory=lambda: ["pdf"])
    language: Optional[str] = "en"
    discussion_blackouts: List[List[str]] = field(default_factory=list)
    discussion_topics: Dict[str, Dict[str, str]] = field(default_factory=dict)
    tabs: List[Tab] = field(default_factory=list)
    user_partitions: List[UserPartition] = field(default_factory=list)

    def to_json(self):
        return json.dumps(self, default=complex_encoder)

@dataclass
class ContentSon:
    name: str
    course: str
    category: str = "asset"
    tag: str = 'cx4'
    org: str = 'edu'
    revision: Optional[str] = None

@dataclass
class Asset:
    contentType: str
    displayname: str
    content_son: ContentSon
    filename: str 
    thumbnail_location: List[Optional[str]]
    locked: bool = False
    import_path: Optional[str] = None

    @staticmethod
    def from_dict(data: dict):
        # Create an Asset instance from a dictionary
        content_son_data = data.pop("content_son", {})
        return Asset(content_son=ContentSon(**content_son_data), **data)


@dataclass
class Grader:
    type: str = field(default_factory=lambda: "Exam")
    min_count: int = field(default_factory=lambda: 3)
    weight: float = field(default_factory=lambda: 1)
    drop_count: int = field(default_factory=lambda: 0)
    short_label: str = field(default_factory=lambda: 'ex')


@dataclass
class GradingPolicy:
    GRADE_CUTOFFS: Dict[str, float] = field(default_factory=lambda: {"Pass": 0.6})
    GRADER: List[Grader] = field(default_factory=lambda: [Grader()])

# Example usage
grading_policy = GradingPolicy()
print(grading_policy)
