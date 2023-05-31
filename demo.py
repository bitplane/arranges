#!/usr/bin/env python3

from pydantic import BaseModel

from arranges import Arranged, Range


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

    some_ranges: Arranged = Arranged("4:5, 15:30, 100:, 4")
    """
    This gets compressed to:

      str(some_ranges) == "5,15:30,100:"

    It's an unbounded range.
    """

    some_more_ranges: Arranged = Arranged([1, 2, 3, 4, range(8, 15), "20:"])
    """
      str(some_more_ranges) == "1:4,8:15,20:"

    You get the idea
    """

    another: Arranged


txt = """
{
    "another": "1:10,20:30,1"
}
"""

x = AnExample.parse_raw(txt)


# you can add ranges together

print(f"{x.some_ranges} + {x.another} == {x.some_ranges + x.another}")

# you can iterate over them or convert to lists
print(f"{list(x.another_range)}")
