# Operators and set methods

Both the `Range` and `Ranges` objects are set-like.

## Cardinality of the address range

The length of a range is the number of elements it contains. But because ranges
can be boundless, we have a special `inf` value that represents an infinite int
as Python doesn't have or support one.

This value is `math.inf`, but when returned from `len` it becomes `sys.maxsize`
as it only supports ints that are this size or smaller. When comparing `inf` to
`sys.maxsize` it'll return `True`, but this doesn't work in all directions:

```python
import math
import sys
from arranges import Ranges, inf

assert len(Range("1,2,3,4,10:20")) == 14

full = Range(":")

assert len(full) == sys.maxsize
assert len(full) == inf
assert sys.maxsize == inf
assert full.stop == inf
assert inf - 100 == sys.maxsize

# Careful though, this does not hold
assert len(full) != math.inf

# because it's an int
assert type(len(full)) is int
```

## Truthyness

Empty ranges are Falsey

```python
from arranges import Range, Ranges

assert Ranges(":")
assert Range(10)

assert not Ranges("")
assert not Range("")
```

## Iterating

You can iterate over a `Range` or `Ranges`

```python
from arranges import Range, Ranges


```

...

```python
from arranges import Range, Ranges, inf

first_100 = Ranges(":100")
next_100 = Range("100:200")
third_100 = Range("200:300")

full_range = Range(":")

# The | operator combines Range or Ranges, returning a new instance.
first_200 = first_100 | next_100

# len() works
assert len(first_100) == len(second_100) == 100
assert len(first_100 | third_100) == 200

# inf is a special value, a float that is equal to as math.inf but returns
# sys.maxsize when returned by len(), which can't be bigger than that.
assert len(full_range) != math.inf
assert len(full_range) == inf
assert len(full_range) == sys.maxsize
assert full_range.stop == inf == math.inf
assert sys.maxsize == inf

# use the in operator to test membership
assert first_100 in first_200




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
