import json
import math
import pickle
import sys

from arranges import inf
from arranges.utils import _Boundless, to_int


def test_is_infinity():
    assert inf == math.inf
    assert math.inf == inf


def test_is_max_size():
    assert inf == sys.maxsize
    assert sys.maxsize == inf


def test_is_bigger_than_max_size():
    assert inf > sys.maxsize
    assert sys.maxsize < inf


def test_inf_minus_one_is_inf():
    assert inf - 1 == inf


def test_inf_minus_one_is_maxsize():
    assert inf - 1 == sys.maxsize


def test_inf_addition():
    """Test addition operations with inf"""
    # inf + number
    assert inf + 5 == inf
    assert inf + 0 == inf
    assert inf + sys.maxsize == inf

    # number + inf (right addition)
    assert 5 + inf == inf
    assert 0 + inf == inf
    assert sys.maxsize + inf == inf

    # Type preservation
    assert isinstance(inf + 5, _Boundless)
    assert isinstance(5 + inf, _Boundless)

    # Test line 71: inf + (-inf) returns NaN (non-infinite)
    neg_inf = float("-inf")
    result = inf + neg_inf
    assert math.isnan(result)
    assert not math.isinf(result)
    assert isinstance(result, float)  # Regular float, not _Boundless


def test_inf_subtraction():
    """Test subtraction operations with inf"""
    # inf - number
    assert inf - 0 == inf
    assert inf - 5 == inf
    assert inf - sys.maxsize == inf

    # number - inf (right subtraction)
    result = 5 - inf
    assert math.isinf(result)
    assert result < 0  # Should be -inf
    assert isinstance(result, _Boundless)

    result = 0 - inf
    assert math.isinf(result)
    assert result < 0
    assert isinstance(result, _Boundless)

    # Edge case: subtraction that would result in NaN
    result = inf - inf
    assert math.isnan(result)  # inf - inf is NaN

    # Test line 62: math.inf - inf returns NaN (non-infinite)
    result = math.inf - inf
    assert math.isnan(result)
    assert not math.isinf(result)
    assert isinstance(result, float)  # Regular float, not _Boundless


def test_inf_string_representation():
    """Test string representations of inf"""
    assert str(inf) == "inf"
    assert repr(inf) == "inf"
    assert f"{inf}" == "inf"


def test_inf_hash():
    """Test that inf is properly hashable"""
    assert hash(inf) == hash(math.inf)

    # Can be used in sets
    s = {inf}
    assert inf in s

    # Can be used as dict key
    d = {inf: "value"}
    assert d[inf] == "value"


def test_inf_index():
    """Test __index__ returns sys.maxsize"""
    assert inf.__index__() == sys.maxsize

    # Should work in slice operations
    test_list = list(range(10))
    assert test_list[: inf.__index__()] == test_list
    assert test_list[:inf] == test_list


def test_inf_type():
    """Test that inf is a float subclass"""
    assert isinstance(inf, float)
    assert isinstance(inf, _Boundless)
    assert type(inf).__name__ == "_Boundless"


def test_inf_comparisons():
    """Test comparison operations"""
    # Greater than
    assert inf > 0
    assert inf > 1000
    assert inf > -1000
    assert inf > float("-inf")

    # Less than (should be False for positive numbers)
    assert not (inf < 1000)
    assert not (inf < sys.maxsize)
    assert not (inf < math.inf)

    # Greater than or equal
    assert inf >= inf
    assert inf >= sys.maxsize
    assert inf >= 0

    # Less than or equal
    assert inf <= inf
    assert not (inf <= 1000)


def test_inf_division():
    """Test division operations with inf"""
    # inf divided by numbers
    assert inf / 2 == math.inf
    assert inf / sys.maxsize == math.inf
    assert isinstance(inf / 2, float)  # Division doesn't preserve _Boundless

    # Numbers divided by inf
    assert 2 / inf == 0.0
    assert sys.maxsize / inf == 0.0
    assert -5 / inf == 0.0


def test_inf_boolean():
    """Test inf in boolean context"""
    assert bool(inf) is True
    assert inf or False
    assert not (not inf)
    if inf:
        pass  # Should execute
    else:
        assert False, "inf should be truthy"


def test_inf_with_builtins():
    """Test inf with built-in functions"""
    # min/max
    assert max(1, 2, inf) == inf
    assert min(1, 2, inf) == 1
    assert max(inf, sys.maxsize) == inf
    assert min(inf, sys.maxsize) == sys.maxsize

    # abs
    assert abs(inf) == inf


def test_inf_sorting():
    """Test inf in sorting operations"""
    items = [5, inf, 2, sys.maxsize, 1, math.inf]
    sorted_items = sorted(items)

    # All equal values should maintain relative order (stable sort)
    # But since inf == sys.maxsize == math.inf, they're all equal
    assert sorted_items == [1, 2, 5, inf, sys.maxsize, math.inf]

    # Reverse sorting
    reverse_sorted = sorted(items, reverse=True)
    assert reverse_sorted[0] in (inf, sys.maxsize, math.inf)
    assert reverse_sorted[-1] == 1


def test_inf_pickle():
    """Test that inf can be pickled and unpickled"""
    pickled = pickle.dumps(inf)
    unpickled = pickle.loads(pickled)

    assert unpickled == inf
    assert unpickled == sys.maxsize
    assert unpickled == math.inf
    assert isinstance(unpickled, _Boundless)


def test_inf_json():
    """Test JSON serialization behavior"""
    # Standard json should handle infinity
    assert json.dumps(float(inf)) == "Infinity"

    # But our custom inf object might behave differently
    # since json.dumps calls __float__ implicitly
    assert json.dumps(inf) == "Infinity"

    # Deserializing back won't give us _Boundless though
    loaded = json.loads(json.dumps(inf))
    assert loaded == float("inf")
    assert not isinstance(loaded, _Boundless)


def test_inf_edge_cases():
    """Test various edge cases"""
    # Multiplication
    assert inf * 2 == math.inf
    assert inf * 0 != inf  # Should be NaN
    assert math.isnan(inf * 0)

    # Power operations
    assert inf**2 == math.inf
    assert inf**0 == 1.0  # Any number to power of 0 is 1

    # Modulo (usually undefined for infinity)
    result = inf % 5
    assert math.isnan(result)

    # Negative inf
    neg_inf = -inf
    assert neg_inf < 0
    assert math.isinf(neg_inf)


def test_to_int_with_start():
    """Test to_int with special 'start' value"""

    # "start" should return 0
    assert to_int("start", 999) == 0
