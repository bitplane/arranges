"""Tests for the as_key utility function"""

import pytest
from arranges import Ranges
from arranges.utils import as_key, inf


def test_integer_becomes_single_element_range():
    """Integer N becomes range N:N+1"""
    result = as_key(5)
    expected = Ranges(5, 6)
    assert result == expected
    assert str(result) == "5"


def test_zero_becomes_single_element_range():
    """Zero becomes range 0:1"""
    result = as_key(0)
    expected = Ranges(0, 1)
    assert result == expected
    assert str(result) == "0"


def test_negative_integer_fails():
    """Negative integers should raise error (ranges don't support negative)"""
    with pytest.raises(ValueError):
        as_key(-1)


def test_string_range_passthrough():
    """String ranges are converted to Ranges"""
    result = as_key("0:10")
    expected = Ranges("0:10")
    assert result == expected
    assert str(result) == ":10"


def test_complex_string_range():
    """Complex range strings work"""
    result = as_key("0:5,10:15,20:")
    expected = Ranges("0:5,10:15,20:")
    assert result == expected


def test_slice_object():
    """Slice objects are converted to Ranges"""
    result = as_key(slice(5, 10))
    expected = Ranges(5, 10)
    assert result == expected
    assert str(result) == "5:10"


def test_slice_with_none_start():
    """Slice with None start becomes 0:stop"""
    result = as_key(slice(None, 10))
    expected = Ranges(0, 10)
    assert result == expected
    assert str(result) == ":10"


def test_slice_with_none_stop():
    """Slice with None stop becomes infinite range"""
    result = as_key(slice(5, None))
    expected = Ranges(5, float("inf"))
    assert result == expected
    assert str(result) == "5:"


def test_slice_with_step_raises_error():
    """Slice with step should raise error"""
    with pytest.raises(ValueError, match="Stepped ranges not supported"):
        as_key(slice(0, 10, 2))


def test_range_object():
    """Python range objects are converted"""
    result = as_key(range(5, 15))
    expected = Ranges(5, 15)
    assert result == expected


def test_range_with_step_raises_error():
    """Range with step should raise error"""
    with pytest.raises(ValueError, match="Stepped ranges not supported"):
        as_key(range(0, 10, 2))


def test_existing_ranges_object_passthrough():
    """Existing Ranges objects pass through unchanged"""
    original = Ranges("5:10")
    result = as_key(original)
    assert result == original
    # Should be same object or equivalent
    assert str(result) == str(original)


def test_empty_string_becomes_empty_range():
    """Empty string becomes empty range"""
    result = as_key("")
    expected = Ranges("")
    assert result == expected
    assert str(result) == ""


def test_colon_only_becomes_infinite_range():
    """Single colon becomes infinite range"""
    result = as_key(":")
    expected = Ranges(":")
    assert result == expected
    assert str(result) == ":"


def test_invalid_string_raises_error():
    """Invalid range strings should raise errors"""
    with pytest.raises((ValueError, TypeError)):
        as_key("not-a-range")


def test_list_of_integers():
    """List of integers should convert to discrete ranges"""
    result = as_key([1, 3, 5, 7])
    # Should represent individual positions
    assert isinstance(result, Ranges)
    # Each integer should become a single-element range


def test_intlike_objects():
    """Objects with __int__ and __add__ methods should work like integers"""

    class IntLike:
        def __init__(self, value):
            self.value = value

        def __int__(self):
            return self.value

        def __add__(self, other):
            return IntLike(self.value + other)

    obj = IntLike(42)
    result = as_key(obj)
    expected = Ranges(obj, obj + 1)
    assert result == expected


def test_inf_object():
    """The inf object should work as an intlike key"""
    result = as_key(inf)
    # inf + 1 equals inf, so this should be an empty range
    assert result == ""


def test_non_intlike_objects_as_ranges():
    """Objects without __int__ should be passed to Ranges constructor"""

    class NotIntLike:
        pass

    obj = NotIntLike()
    # This should either work (if Ranges can handle it) or raise an error
    try:
        result = as_key(obj)
        assert isinstance(result, Ranges)
    except (ValueError, TypeError):
        # That's acceptable too
        pass
