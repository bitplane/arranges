import sys
from typing import Any, Union

from arranges.utils import inf, is_int, is_iterable, is_range, to_int


class Range:
    """
    A single range of values
    """

    start: int = 0
    stop: int = sys.maxsize

    def __init__(self, value: Any = None, stop: int = None, start: int = None):
        """
        Construct a range from a value, start and stop, or a value and stop, similar to Python slice
        and range notation, but with no step and no negative ranges.

        If `value` is a string, it'll expect slice notation, e.g. "100:" or "1:10". Hex, octal and
        binary numbers are supported, along with "start", "inf" and "end" which are considered None
        and 0 respectively. An empty string is treated to be an empty range, and ":" is the full
        range.

        If the `value` is an object that has `start` and `stop` attributes then it'll use those
        values for the start and stop positions, so you can use `range` or `slice` or another `Range`
        if you like. If it's an integer, it'll use that as the stop value and the start defaults to 0.
        """
        has_no_params = value is stop is start is None
        value_only = value is not None and (stop is start is None)
        start_value_and_stop = value is not None and stop is not None
        inconsistent = value is not None and start is not None

        if inconsistent:
            raise ValueError("Got two values for start position")

        if has_no_params:
            raise ValueError("Expected at least one argument, got 0")

        if start_value_and_stop:
            self.start = value
            self.stop = stop

        elif value_only:
            if is_range(value):
                self.start = 0 if value.start is None else value.start
                self.stop = inf if value.stop is None else value.stop
            elif isinstance(value, str):
                other = self.parse_str(value)
                self.start = other.start
                self.stop = other.stop
            else:
                self.start = 0
                self.stop = value
        else:
            self.start = start or 0
            self.stop = inf if stop is None else stop

        # Convert to integers
        self.start = int(self.start)
        if self.stop is not inf:
            self.stop = int(self.stop)

        if self.start < 0 or self.stop < 0:
            raise ValueError("Start and stop must be positive")

        if self.start > self.stop:
            raise ValueError("Stop can't be before start")

        super().__init__()

    @classmethod
    def parse_str(cls, value: str) -> "Range":
        """
        Construct Range from a string, Python slice notation
        """
        vals = [v.strip() for v in str(value).split(":")]

        if len(vals) > 2:
            raise ValueError("Too many values, Only start and stop are allowed")

        if len(vals) == 1:
            start = 0
            stop = to_int(vals[0], 0)
        else:
            # start:stop
            start = to_int(vals[0], 0)
            stop = to_int(vals[1], inf)

        return cls(start=start, stop=stop)

    def __repr__(self):
        """
        Python representation
        """
        name = self.__class__.__name__
        if not self:
            return f"{name}(0, 0)"
        if not self.start and self.stop is inf:
            return f"{name}(0, inf)"
        if self.start == 0:
            return f"{name}({self.stop})"

        return f"{name}({self.start}, {self.stop})"

    def __str__(self):
        """
        Convert to a string
        """
        if not self:
            return ""
        if not self.start and self.stop == inf:
            return ":"
        if self.start == 0:
            return f"{self.stop}"
        if self.stop == inf:
            return f"{self.start}:"

        return f"{self.start}:{self.stop}"

    def __hash__(self) -> int:
        return hash(str(self))

    def __eq__(self, other: Any) -> bool:
        """
        Compare two ranges
        """
        if is_int(other):
            return self.start == other and self.stop == other + 1
        if isinstance(other, str):
            return self == self.parse_str(other)
        if not is_range(other):
            return str(self) == str(other)
        if not self and not other:
            return True
        if not isinstance(other, Range):
            return self == Range(other)

        return self.start == other.start and self.stop == other.stop

    def __lt__(self, other: Any) -> bool:
        """
        Just for sorting. Makes no claims about the ranges being comparable
        """
        if is_range(other):
            start = self.start or 0
            other_start = other.start or 0

            return start < other_start

        return self.start < other

    def __contains__(self, other: Any) -> bool:
        """
        See if a value is in this range
        """
        if is_int(other):
            return self.start <= other <= self.last

        if not self:  # nothing fits in an empty range
            return False

        if is_range(other):
            if not other:
                return True  # the empty set is a subset of all sets

            inf_stop = other.stop or inf
            start_inside = not self.start or other.start in self
            last_inside = self.stop is None or (inf_stop - 1) in self

            return start_inside and last_inside

        if isinstance(other, str):
            return self.parse_str(other) in self

        if is_iterable(other):
            for o in other:
                if o not in self:
                    return False
            return True

        raise TypeError(f"Unsupported type {type(other)}")

    def __add__(self, other: Any) -> "Range":
        """
        Join two ranges together, if possible, and return a new one
        """
        return self.join(other)

    def __iter__(self):
        """
        Iterate over the values in this range
        """
        i = self.start
        while i < self.stop:
            yield i
            i += 1

    def __len__(self) -> Union[int, float]:
        """
        Get the length of this range
        """
        if self.start == self.stop:
            return 0

        return self.stop - self.start

    def __bool__(self) -> bool:
        """
        True if this range has a length
        """
        return len(self) > 0

    @property
    def last(self) -> int:
        """
        Gets the last value in this range. Will return inf if the range
        has no end, and -1 if it has no contents,
        """
        if not self:
            return -1
        return self.stop - 1

    def overlaps(self, other: "Range") -> bool:
        """
        True if this range overlaps with the other range.
        """
        if self in other or other in self:
            return True

        if self.start in other or other.start in self:
            return True

        return False

    def adjacent(self, other: "Range") -> bool:
        """
        True if this range is adjacent to the other range
        """
        if self.stop == other.start or other.stop == self.start:
            return True

        return False

    def attached(self, other: "Range") -> bool:
        """
        True if this range is adjacent or overlaps the other range, and so they
        can be joined together.
        """
        return self.adjacent(other) or self.overlaps(other)

    def join(self, other: "Range") -> "Range":
        """
        Return a new range that is the combination of this range and the other
        """
        if not other:
            return self
        if not self:
            return other

        if not self.attached(other):
            raise ValueError(f"{self} and {other} aren't touching")

        start = min(self.start, other.start)
        stop = max(self.stop, other.stop)

        return Range(start, stop)

    @classmethod
    def validate(cls, value: Any) -> "Range":
        """
        Validate a value and convert it to a Range
        """
        if isinstance(value, cls):
            return value

        if isinstance(value, str):
            return cls.parse_str(value)

        return cls(value)

    @classmethod
    def __get_validators__(cls):
        yield cls.validate
