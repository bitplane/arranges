#!/usr/bin/env python3

from pydantic import BaseModel

from arange import Range, Ranges


class AnExample(BaseModel):
    """ """

    a_range: Range = Range(":50")
    """
    Validator runs converts the string into a range. This is
    0-49 inclusive.
    """

    another_range: Range = Range(range(10, 35))
    """
    You can create them from actual ranges if you like.
    """

    some_ranges: Ranges = Ranges("4:5, 15:30, 100:, 4")
    """
    This gets compressed to:

      str(some_ranges) == "5,15:30,100:"

    It's an unbounded range.
    """

    some_more_ranges: Ranges = Ranges([1, 2, 3, 4, range(8, 15), "20:"])
    """
      str(some_more_ranges) == "1:4,8:15,20:"

    You get the idea
    """

    another: Ranges


txt = """
{
    "another": "1:10,20:30,1"
}
"""

x = AnExample.parse_raw(txt)

print(f"{x.some_ranges} + {x.another} == {x.some_ranges + x.another}")
