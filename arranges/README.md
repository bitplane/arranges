# A Range - Range strings for Pydantic BaseModels

I needed a way to specify batches of byte, row and line ranges in my
`merge-files`  app, and the more I messed with it the more it grew into a
monster. So I've split it out into a separate package.

## Installation

`pip install arranges`, or clone the repo and `pip install ./arranges` from the
root of the repo. Or `make dev` and `code .` to open the project in a venv
in vscode.

## Usage

Construct a `Range` or `Ranges` object from a `str`, list of `int`s, or
anything with `start` and `stop` attributes (`range`s, `slice`s or similar),
and get an object you can iterate over, test membership, combine and do other
things with.

```python

from arranges import Ranges


## Constraints

I'm using them for 

```bash

```python
from pydantic import BaseModel

from arranges import Range, Ranges


class AnExample(BaseModel):
    """

    """

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
```
