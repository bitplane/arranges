import re
from functools import lru_cache
from typing import Any, Iterable

from arranges.segment import Segment, range_idx
from arranges.utils import is_intlike, is_iterable, is_rangelike, try_hash


class Range(str):
    """
    A range set that can be hashed and converted to a string.
    """

    segments: tuple[Segment]
    step: int = 1

    def __init__(self, value: Any, stop: range_idx | None = None):
        """
        Construct a new string with the canonical form of the range.
        """
        self.segments = self.from_str(self)

    def __new__(cls, value: Any, stop: range_idx | None = None) -> str:
        """
        Construct a new string with the canonical form of the range.

        This becomes "self" in __init__, so we're always a string
        """
        return str.__new__(cls, cls.construct_str(value, stop))

    @classmethod
    def construct_str(cls, value, stop) -> str:
        """
        Create a string representation of a range series
        """
        start_and_stop = value is not None and stop is not None
        stop_only = value is None and stop is not None

        if start_and_stop or stop_only:
            return Segment(value, stop)

        if value is None:
            raise TypeError("Got 0 arguments, expected 1 or 2")

        if is_intlike(value):
            return Segment(0, value)

        if is_rangelike(value):
            if not value.step or value.step == 1:
                return Segment(value.start, value.stop)
            else:
                stepped_range = list(value)
                return cls.iterable_to_str(stepped_range)

        if hasattr(value, "segments"):
            return ",".join(value.segments)

        if isinstance(value, str):
            normalized = cls.from_str(value)
            return ",".join(str(v) for v in normalized)

        if is_iterable(value):
            return cls.iterable_to_str(value)

        raise TypeError(f"Cannot convert {value} into {cls.__name__}")

    @staticmethod
    def split_str(value: str) -> list[str]:
        return re.split(r",|;", value)

    @classmethod
    def from_str(cls, value: str) -> tuple[Segment]:
        """
        Construct from a string.
        """
        ret = []

        for s in cls.split_str(value):
            ret.append(Segment.from_str(s))

        cacheable = tuple(set(ret))

        return cls.from_hashable_iterable(cacheable)

    @classmethod
    def iterable_to_str(cls, iterable: Iterable) -> str:
        """
        Convert an iterable of ranges to a string
        """
        hashable = tuple(iterable)
        if try_hash(hashable):
            vals = cls.from_hashable_iterable(hashable)
        else:
            vals = cls.from_iterable(hashable)

        return ",".join(str(v) for v in vals)

    @classmethod
    @lru_cache
    def from_hashable_iterable(cls, value: tuple[Segment]) -> tuple[Segment]:
        """
        Cache the result of from_iterable
        """
        return cls.from_iterable(value)

    @staticmethod
    def _flatten(iterable: Iterable) -> Iterable[Segment]:
        """
        Flatten into RangeSegments
        """
        for item in iterable:
            if isinstance(item, Segment):
                yield item
            if isinstance(item, Range):
                yield from item.segments
            elif isinstance(item, str):
                if item:
                    yield from [Segment.from_str(s) for s in Range.split_str(item)]
            elif is_iterable(item):
                yield from Range._flatten(item)
            elif is_intlike(item):
                yield Segment(item, item + 1)
            else:
                yield from Range(item).segments

    @classmethod
    def from_iterable(cls, iterable: Iterable) -> tuple[Segment]:
        """
        Sort and merge a list of ranges.
        """
        segments: list[Segment] = []
        segments.extend(cls._flatten(iterable))
        segments.sort(key=Segment.sort_key)

        i = 1

        while i < len(segments):
            current = segments[i]
            last = segments[i - 1]
            if last.isconnected(current):
                segments[i - 1] = current.union(last)
                del segments[i]
                i -= 1
            i += 1

        return tuple(segments)

    def __hash__(self):
        return super().__hash__()

    def __add__(self, other):
        s = self.iterable_to_str(tuple([self, other]))
        return Range(s)

    def __eq__(self, other: Any) -> bool:
        """
        Compare the two lists based on their string representations
        """
        if not isinstance(other, Range):
            other = Range(other)
        return super().__eq__(other)

    def __contains__(self, other: Any) -> bool:
        """
        Are all of the other ranges in our ranges?
        """
        combined = str(self + other)
        return self and combined == self

    def __iter__(self):
        """
        Iterate over the values in our ranges.

        Note that this could be boundless.
        """
        for r in self.segments:
            for i in r:
                yield i

    def intersects(self, other: Any) -> bool:
        """
        True if this range overlaps with the other range
        """
        other: Range = Range(other)
        for r in self.segments:
            for o in other.segments:
                if r.intersects(o):
                    return True

        return False

    def union(self, other) -> "Range":
        """
        Return the union of this range and the other
        """
        return Range(self + other)

    def __or__(self, other: "Range") -> "Range":
        """
        Return the union of this range and the other
        """
        return self.union(other)

    @classmethod
    def validate(cls, value: Any) -> "Range":
        """
        Validate a value and convert it to a Range
        """
        if isinstance(value, cls):
            return value

        return cls(value)

    @classmethod
    def __get_validators__(cls):
        """
        For automatic validation in pydantic
        """
        yield cls.validate

    @property
    def first(self):
        return self.segments[0].start

    @property
    def last(self):
        return self.segments[-1].last
