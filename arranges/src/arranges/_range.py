# from typing import Any

# from arranges.segment import Segment
# from arranges.utils import as_type, inf, is_intlike, is_iterable, is_rangelike, to_int


# class Range:
#     """
#     A range of numbers, similar to Python slice notation, but with no step or
#     negative/relative ranges.
#     """

#     start: int = 0
#     stop: int = inf

#     def isdisjoint(self, other: Any) -> bool:
#         """
#         Return True if this range is disjoint from the other range
#         """
#         other = as_type(Range, other)
#         return not self.intersects(other)

#     def issubset(self, other: Any) -> bool:
#         """
#         Return True if this range is a subset of the other range
#         """
#         other = as_type(Range, other)
#         return self in other

#     def __le__(self, other: Any) -> bool:
#         """
#         Return True if this range is a subset of the other range
#         """
#         other = as_type(Range, other)
#         return self in other

#     def __lt__(self, other: Any) -> bool:
#         """
#         Return True if this range is a proper subset of the other range
#         """
#         other = as_type(Range, other)
#         return self in other and self != other

#     def issuperset(self, other: Any) -> bool:
#         """
#         Return True if this range is a superset of the other range
#         """
#         other = as_type(Range, other)
#         return other in self

#     def __ge__(self, other: Any) -> bool:
#         """
#         Return True if this range is a superset of the other range
#         """
#         other = as_type(Range, other)
#         return other in self

#     def __gt__(self, other: Any) -> bool:
#         """
#         Return True if this range is a proper superset of the other range
#         """
#         other = as_type(Range, other)
#         return other in self and self != other

#     def __invert__(self) -> "Range":
#         """
#         Return the inverse of this range (compliment)
#         """
#         if not self:
#             return Range(0, inf)

#         if self.start == 0:
#             return Range(self.stop, inf)

#         if self.stop == inf:
#             return Range(0, self.start)

#         raise ValueError("Inverting this range will cause a discontinuity")

#     def __and__(self, other: "Range") -> "Range":
#         """
#         Return the intersection of this range and the other range
#         """
#         return self.intersection(other)

#     def __sub__(self, other: "Range") -> "Range":
#         """
#         Return the difference between this range and the other
#         """
#         if not self.intersects(other):
#             return Range(self)

#     # def difference(self, *others):
#     #     """
#     #     Remove the other ranges from this one
#     #     """
#     #

#     # def symmetric_difference(self, other: "Range") -> "Range":
#     #     """
#     #     Return the symmetric difference of two ranges
#     #     """

#     # def __xor__(self, other: "Range") -> "Range":
#     #     """
#     #     Return the symmetric difference of two ranges
#     #     """
