"""
Some quacky type helpers so we don't have to use isinstance everywhere
"""
import sys
from typing import Any, Type, TypeVar

T = TypeVar("T")


class _Boundless(int):
    """
    A class that represents a boundless end of a range
    """

    def __repr__(self) -> str:
        return "inf"

    def __gt__(self, other):
        return True

    def __lt__(self, other):
        return False

    def __eq__(self, other):
        return super().__eq__(other)

    def __sub__(self, value: int) -> int:
        return self

    def __add__(self, value: int) -> int:
        return self


inf = _Boundless(sys.maxsize)


def to_int(value: str, default: int) -> int:
    """
    Convert a string to an integer. If the string is empty, return the default
    """
    if not value:
        return default
    try:
        return int(value)
    except ValueError:
        if "0x" in value:
            return int(value, 16)
        elif "0o" in value:
            return int(value, 8)
        elif "0b" in value:
            return int(value, 2)
        elif value in ("inf", "end"):
            return sys.maxsize
        elif value == "start":
            return 0
        else:
            raise ValueError(f"Invalid integer value {value}")


def is_rangelike(value: Any) -> bool:
    """
    Check if a value is a range-like object
    """
    return hasattr(value, "start") and hasattr(value, "stop")


def is_intlike(value: Any) -> bool:
    """
    Can this object be converted to an integer?
    """
    return hasattr(value, "__int__")


def is_iterable(value: Any) -> bool:
    """
    Is this object iterable?
    """
    return hasattr(value, "__iter__")


def as_type(cls: Type[T], value: Any) -> T:
    """
    Convert a value to a type, if necessary.

    Saves a bit of construction time if the value is already the right type.
    """
    if isinstance(value, cls):
        return value
    return cls(value)
