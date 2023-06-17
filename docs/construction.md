# Constructing Range and Ranges

You can create them from:

1. strings
2. range-like objects
3. sequences of ints or these things, or other sequences
4. explicitly, like you would create a `range` or `slice`

Essentially, the constructor has `value` and `stop` fields. If `stop` is
provided then `value` is assumed to be the `start`, otherwise it's assumed
you want to convert the `value` from something else.

## Range from a string

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
gbc_palette = Range("0xff68:0xff88")
skip_bmp_header = Range("0o66:end")  # skip "54", "0x36" or "0b1100110" bytes

# "end" and "inf" are the same. You can also use "start" instead of 0.
the_full_range_again = Range("start:inf")

# whitespace is ignored during construction
first_kilobyte = Range("start : 0x400")

# They are simplified when converted to str, which they can be compared with.
assert first_kilobyte == ":1024"

# Comparisons work in both directions
assert "000001:000002" == Range("1")

# and the hash is the same as the string
w = Range("6 : 8")
assert hash(w) == hash("6:8")

# so you can use them as dict keys
d = {"6:8": "width"}
d[w] = "GIF file width"
assert d == {"6:8": "GIF file width"}
```

## Ranges from a string

```python
from arranges import Ranges

# You can put gaps in your range using commas.
pages_2_to_5_and_20 = Ranges("2:6, 20")

# The ranges are sorted and combined as they are added
overlapping = Ranges("start:10, 14, 1:3")
assert overlapping == ":10,14"

# But you can't hash Ranges because they're mutable
import pytest

with pytest.raises(ValueError):
    a = {overlapping: "whatever"}
```

## Ranges from range-like objects

If it has a start, stop and step attribute then it quacks like a range so you
can pass it in as the value. If the `step` value is something other than None
or 1 then it'll raise `ValueError`.

```python
from arranges import Range

from_slice = Range(slice(10, 20))
from_range = Range(range(10, 20))
from_other = Range(Range("10:20"))

assert from_slice == from_range == from_other == "10:20"
```

## Ranges from sequences

When creating a Range object from a sequence, it'll have to be in sequential
order with no gaps. Duplicates are absorbed.

```python
from arranges import Range

l = list(range(100))
t = tuple(range(100))
i = (i for i in range(100))

assert Range(l) == Range(t) == Range(i) == ":100"
```

`Ranges` are much more forgiving:

```python
from arranges import Ranges

jumble = Ranges([0, [2, 4], ["1:3"], 3, 4, range(10, 20)])

assert jumble == "5,10:20"
```

## Explicitly creating a Range

You can create them in the same way as `range` or `slice` objects which have a
slightly different syntax to slice notation.

```python
from arranges import Range, inf

assert Range(10, inf) == "10:"

# Range("10") is not the same as Range(10)
assert Range(10) == ":10"
assert Range("10") == 10 == Range(10, 11)
```
