from enum import Enum

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

class DescriptorType(Enum):
    COURSE = "COURSE"
    MODULE = "MODULE"