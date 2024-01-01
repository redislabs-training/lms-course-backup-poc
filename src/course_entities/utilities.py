import logging
import re
from enum import Enum

SEMVER_REGEX = r"^v?(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$"


def convert_enum(value: str, enum_class: Enum):
    """
    Convert a string to an enum type, given the string and enum class.

    Parameters:
        value (str): The string representation of the enum member.
        enum_class (Enum): The class of the target enum.

    Returns:
        Enum: The corresponding enum member.

    Raises:
        TypeError: If the value cannot be converted to the given enum type.
    """
    if isinstance(value, str):
        logging.debug(f"Converting string '{value}' to {enum_class.__name__} enum type")
        try:
            return enum_class[value]
        except KeyError:
            raise ValueError(f"{value} is not a valid member of {enum_class.__name__}")
    
    if not isinstance(value, enum_class):
        raise TypeError(f"value must be an instance of {enum_class.__name__} enum")
    
    return value



def validate_semver(version: str):
    """
    Validate a course version.

    Parameters:
        version (str): The string representation of the version.

    Returns:
        Void

    Raises:
        ValueError: If the value cannot be converted to the given enum type.
    """
    if not re.match(SEMVER_REGEX, version):
        raise ValueError(f"{version} is not a valid Semantic Version with 'v' prefix")