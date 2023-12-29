from dataclasses import dataclass
from .topic import CourseTopic
from .module import CourseModule

    
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
            "visibility": self.visibility.name,
            "type": self.type.name,
            "module": self.module.to_dict()
        }