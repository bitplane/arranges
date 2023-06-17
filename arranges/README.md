# Arranges

## Range string fields for Pydantic BaseModels

I needed a way to parse batches of byte, row and line and other object ranges
in my `merge-files` app, in a way that I can just drop it in as a string field
type. The reason for this is so the machine-generated command line help is
flat and readable by humans.

It it kinda grew into a monster so I've split it out into this separate
package. It gives a couple of classes for dealing with ranges:

* `Range`, a class that can be constructed from Python-style slice notation
  strings (e.g. `"1:10"`, `"0x00:0xff`, `":"`), range-likes, iterables of
  int-like objects. It has convenient properties lke being iterable, immutable,
  has a stable string representation and matching hash, it can be treated
  like a `set` and its constructor is compatible with `range` and `slice`.
* The `Ranges` class is similar but supports holes in ranges - it's an ordered,
  mutable list of non-overlapping `Range` objects that simplifies as data is
  added.

## Constraints

I made it to select lines or bytes in a stream of data, so it:

* only supports `int`s;
* does not allow negative indices, the minimum is 0 and the maximum is
  unbounded;
* it's compatible with `range` and `slice`, but `step` is fixed to `1`. This
  may change in the future;
* does not support duplicate ranges. Ranges are merged together as they are
  added to the `Ranges` object;
* it is unpydantic in that its constructors are duck-typed, which is what I
  need; and
* it violates the Zen of Python by having multiple ways to do the same thing,
  but it's also useful.
* Currently the interface is *unstable*, so lock the exact version in if you
  don't want breaking changes.

## Installation

`pip install arranges` if you want to use it. You'll need Python 3.10 or
above.

### Developing

To add features etc you'll ideally need `git`, `make`, `bash` and something
with a debugger. Config for Visual Studio Code is included.

Clone the repo and `make dev` to make the venv, install dependencies, then
`code .` to open the project up in the venv with tests and debugging and all
that jazz.

Type `make help` to see the other options, or run the one-liner scripts in the
`./build` dir if you want to run steps without all that fancy caching nonsense.

## Usage Examples

Step through [../demo.py](`./demo.py`) in the debugger to see what's going on,
or read the tests.

### Range from a string

```python
from arranges import Range

# Create a range from a string. Like a slice but without the square brackets.
the_full_range = Range(":")  # an endless sequence starting at 0
the_empty_range = Range("")  # start, stop and len() are all 0
from_0_to_99 = Range("0:100")
skip_10_items = Range("10:")  # boundless, goes to infinity
access_by_index = Range("0")  # just the first item

# Decimal, hexadecimal, octal and binary are supported. Note that octal uses
# Python's 0o prefix, not 0 like in C.
gbc_palette = Ranges("0xff68:0xff88")
skip_bmp_header = Ranges("0o66:end")  # skip "54", "0x36" or "0b1100110" bytes

# "end" and "inf" are the same. You can also use "start" instead of 0.
the_full_range_again = Ranges("start:inf")

# whitespace is ignored during construction
first_kilobyte = Range("start : 0x400")

# They are simplified when converted to str, which they can be compared with.
assert first_kilobyte == ":255"

# and the hash is the same as the string
w = Range("6 : 8")
assert hash(w) == hash("6:8")

# so you can use them as dict keys
d = {"6:8": "width"}
d[w] = "GIF file width"
assert d == {"6:8": "GIF file width"}
```

### Ranges from a string

```python
from arranges import Ranges

# You can put gaps in your range using commas.
pages_2_to_5_and_20 = Ranges("2:6, 20")

# The ranges are sorted and combined as they are added
overlapping = Ranges("start:10, 0xe:0xf, 1:3")
assert overlapping == ":10,14:16"

# But you can't hash Ranges because they're mutable
import pytest

with pytest.raises(ValueError):
    a = {overlapping: "whatever"}
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

#
```

### Operators and methods

```python
from arranges import Range, Ranges, inf

first_100 = Ranges(":100")
next_100 = Range("100:200")
third_100 = Range("200:300")

full_range = Range(":")

# The | operator combines Range or Ranges. Like in sets it returns a new
# instance.
first_200 = first_100 | next_100

# len() works
assert len(first_100) == len(second_100) == 100

# Infinity is a special value, an integer that masquerades as math.inf
assert len(full_range) == math.inf
assert len(full_range) == inf

assert first_200 == "200" # works if the right side is in canonical form
assert first_100 in first_200 # use the in operator to test membership
# assert first_100 < next_100 # less than is only used for ordering
# assert len(first_200) == 200 # len() returns the number of items in the range

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
