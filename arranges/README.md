# Arranges

## Range strings for Pydantic BaseModels

I needed a way to specify batches of byte, row and line ranges in my
`merge-files` app. It it kinda grew into a monster so I've split it out into
a separate package. It arranges and merges ranges, and the name "arranger"
was already taken so I've called it `arranged`.

## Installation

`pip install arranged`, or clone the repo and `make dev` to make the venv,
install dependencies, then `code .` to open the project up in the venv with
debugging and all that jazz.

Type `make help` to see the other options, or run the one-liner scripts in the
`./build` dir if you want to do stuff without all that fancy caching stuff.

## Usage

Construct a `Arranged` or `Ranges` object from a `str`, list of `int`s, or
anything with `start` and `stop` attributes (`range`s, `slice`s or similar),
and get an object you can iterate over, test membership, combine and do other
things with.

Step through [../demo.py](`./demo.py`) in the debugger to see what's going on.

## Constraints

I made it to select lines or bytes in a stream of data, so it:

* only supports `int`s;
* does not allow negative indices, the minimum is 0 and the maximum is
  unbounded;
* does not support step values, only start and stop values; and
* does not support duplicate ranges. Ranges are merged together as they are
  added to the `Arranged` object.

## Examples

### Ranges as strings

```python
from arranges import Ranges

# Create a range from a string. Like a slice but without the square
# brackets.
the_full_range = Ranges(":") # an endless sequence starting at 0
the_empty_range = Range("")
from_0_to_99 = Ranges("100")  # the same as ":100"
skip_10_items = Ranges("10:")
from_100_to_199 = Ranges("100:200")

# Decimal, hexadecimal, octal and binary are supported. Note that octal uses
# Python's 0o prefix, not 0 like in C.
gbc_palette = Ranges("0xff68:0xff88")
skip_bmp_header = Ranges("0o66:end")  # skip "54", "0x36" or "0b1100110" bytes

# "end" and "inf" are the same. You can also use "start" instead of 0.
the_full_range_again = Ranges("start:inf")

# You can put gaps in your range using commas. Spaces are ignored.
pages_2_to_5_and_20 = Ranges("2:6, 20:20")

# The ranges are sorted and combined as they are added, an dthe `str` of the
# range is consistant and always displayed in decimal format with no spaces.
# The hash value of the range is the hash of its `str` value, so they are safe
# to cache if you don't mutate them.
# They compare with strings as long as the string is in canonical form:
assert Ranges("start:10, 1:3, 0xe:0xf") == "10,14:16"
```

### Ranges from other things

```python
from arranges import Ranges

# You can create a range from anything that has a start and stop attribute,
# like so:
assert Ranges(slice(10, 20)) == Ranges(range(10, 20)) == "10:20"

# Ints are just a range that spans one integer, and sequences containing
# them are combined into a Ranges object:
assert Ranges([0, ["1:3"], 3, 4, range(10, 20)]) == "5,10:20"
```

### Operators and methods

```python
from arranges import Ranges

first_100 = Ranges("100")
next_100 = Ranges("100:200")

# The + operator combines ranges:
first_200 = first_100 + next_100

assert first_200 == "200" # works if the right side is in canonical form
assert first_100 in first_200 # use the in operator to test membership
assert first_100 < next_100 # less than is only used for ordering
assert len(first_200) == 200 # len() returns the number of items in the range
assert not Range("") # empty ranges are falsey

assert not first_100.overlaps(next_100) # use overlaps() to test for overlap
assert first_100.adjacent(next_100) # use adjacent() to test for adjacency
assert first_100.adjacent(

# todo:
#
# use "-" to remove a range from another
# implement & operator
# implement | operator
#



len(s)                       - number of elements in set s (cardinality)
x in s                       - test for membership

x not in s                   - all not in
isdisjoint(other)

issubset(other)              - all in
set <= other

set < other                  - not equal, but all in

issuperset(other)            -
set >= other                 - all in

set > other                  - >= and not ==

union(*others)               - combine them (plus)
set | other

intersection(*others)        -
set & other

difference(*others)          - remove it
set - other

symmetric_difference(other)  - in either but not both.
set ^ other
```

```python
from arranges import Ranges
```

## API Docs

## License

WTFPL with one additional clause: don't blame me. Free as in freedom from
legalese.
