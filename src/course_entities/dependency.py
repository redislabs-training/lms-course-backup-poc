from dataclasses import dataclass

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