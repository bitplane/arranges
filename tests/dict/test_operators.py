"""Test Dict operators and comparison methods"""

import pytest
from arranges import Dict


def test_equality_operator():
    """Test __eq__ operator"""
    d1 = Dict()
    d1[100:200] = "highlight"
    d1[300:400] = "selection"

    d2 = Dict()
    d2[100:200] = "highlight"
    d2[300:400] = "selection"

    d3 = Dict()
    d3[100:200] = "different"
    d3[300:400] = "selection"

    # Same contents should be equal
    assert d1 == d2
    assert d2 == d1

    # Different contents should not be equal
    assert not (d1 == d3)
    assert not (d3 == d1)

    # Empty dicts should be equal
    empty1 = Dict()
    empty2 = Dict()
    assert empty1 == empty2


def test_inequality_operator():
    """Test __ne__ operator"""
    d1 = Dict()
    d1[100:200] = "highlight"

    d2 = Dict()
    d2[100:200] = "highlight"

    d3 = Dict()
    d3[100:200] = "different"

    # Same contents should not be unequal
    assert not (d1 != d2)

    # Different contents should be unequal
    assert d1 != d3
    assert d3 != d1


def test_equality_with_regular_dict():
    """Test equality with regular dict"""
    d = Dict()
    d[100:200] = "highlight"
    d[300:400] = "selection"

    # Should be equal to regular dict with same key-value pairs
    regular_dict = {"100:200": "highlight", "300:400": "selection"}
    assert d == regular_dict
    assert regular_dict == d

    # Should not be equal to different regular dict
    different_dict = {"100:200": "different", "300:400": "selection"}
    assert d != different_dict
    assert different_dict != d


def test_union_operator():
    """Test __or__ (|) operator for dict union"""
    d1 = Dict()
    d1[100:200] = "highlight"
    d1[300:400] = "selection"

    d2 = Dict()
    d2[500:600] = "new_range"
    d2[300:400] = "override"  # Should override d1's value

    # Union should combine both dicts, with d2 values taking precedence
    result = d1 | d2

    assert isinstance(result, Dict)
    assert result[100:200] == "highlight"  # From d1
    assert result[300:400] == "override"  # From d2 (overrides d1)
    assert result[500:600] == "new_range"  # From d2
    assert len(result) == 3

    # Original dicts should be unchanged
    assert d1[300:400] == "selection"
    assert len(d1) == 2


def test_union_with_regular_dict():
    """Test union operator with regular dict"""
    d = Dict()
    d[100:200] = "highlight"

    regular_dict = {"300:400": "selection", "500:600": "new"}

    # Dict | regular_dict should work
    result = d | regular_dict
    assert isinstance(result, Dict)
    assert result[100:200] == "highlight"
    assert result[300:400] == "selection"
    assert result[500:600] == "new"

    # regular_dict | Dict should also work (if supported)
    try:
        result2 = regular_dict | d
        assert isinstance(result2, dict)  # Should be regular dict
        assert result2["100:200"] == "highlight"
        assert result2["300:400"] == "selection"
    except TypeError:
        # This might not work depending on Python version
        pass


def test_inplace_union_operator():
    """Test __ior__ (|=) operator for inplace union"""
    d1 = Dict()
    d1[100:200] = "highlight"
    d1[300:400] = "selection"

    d2 = Dict()
    d2[500:600] = "new_range"
    d2[300:400] = "override"

    original_d1 = id(d1)

    # Inplace union should modify d1
    d1 |= d2

    assert id(d1) == original_d1  # Same object
    assert d1[100:200] == "highlight"
    assert d1[300:400] == "override"  # Overridden by d2
    assert d1[500:600] == "new_range"
    assert len(d1) == 3


def test_inplace_union_with_regular_dict():
    """Test inplace union with regular dict"""
    d = Dict()
    d[100:200] = "highlight"

    regular_dict = {"300:400": "selection", "100:200": "override"}

    d |= regular_dict

    assert d[100:200] == "override"
    assert d[300:400] == "selection"
    assert len(d) == 2


def test_comparison_operators_not_supported():
    """Test that comparison operators raise appropriate errors"""
    d1 = Dict()
    d1[100:200] = "highlight"

    d2 = Dict()
    d2[300:400] = "selection"

    # Dicts don't support ordering comparisons
    with pytest.raises(TypeError):
        d1 < d2

    with pytest.raises(TypeError):
        d1 <= d2

    with pytest.raises(TypeError):
        d1 > d2

    with pytest.raises(TypeError):
        d1 >= d2


def test_bool_operator():
    """Test __bool__ operator (truthiness)"""
    empty_dict = Dict()
    assert not bool(empty_dict)
    assert not empty_dict  # Implicit bool conversion

    non_empty_dict = Dict()
    non_empty_dict[100:200] = "highlight"
    assert bool(non_empty_dict)
    assert non_empty_dict  # Implicit bool conversion


def test_len_operator():
    """Test __len__ operator"""
    d = Dict()
    assert len(d) == 0

    d[100:200] = "highlight"
    assert len(d) == 1

    d[300:400] = "selection"
    assert len(d) == 2


def test_iter_operator():
    """Test __iter__ operator (iteration over keys)"""
    d = Dict()
    d[100:200] = "highlight"
    d[300:400] = "selection"

    keys = list(d)  # Uses __iter__
    assert len(keys) == 2
    assert "100:200" in keys
    assert "300:400" in keys

    # Test explicit iteration
    collected_keys = []
    for key in d:
        collected_keys.append(key)

    assert set(collected_keys) == set(keys)


def test_reversed_operator():
    """Test __reversed__ operator"""
    d = Dict()
    d[100:200] = "first"
    d[300:400] = "second"
    d[500:600] = "third"

    # Get keys in insertion order
    forward_keys = list(d.keys())

    # Get keys in reverse order
    reversed_keys = list(reversed(d))

    assert len(reversed_keys) == len(forward_keys)
    assert reversed_keys == list(reversed(forward_keys))


def test_repr_operator():
    """Test __repr__ operator"""
    d = Dict()
    d[100:200] = "highlight"
    d[300:400] = "selection"

    repr_str = repr(d)

    # Should be a valid representation
    assert isinstance(repr_str, str)
    # Should contain the class name and key-value info
    # Exact format may vary, but should be informative


def test_union_empty_dicts():
    """Test union operations with empty dicts"""
    d = Dict()
    d[100:200] = "highlight"

    empty = Dict()

    # Dict | empty should equal original
    result = d | empty
    assert result == d
    assert len(result) == 1

    # empty | Dict should equal Dict
    result2 = empty | d
    assert result2 == d
    assert len(result2) == 1

    # empty | empty should be empty
    result3 = empty | Dict()
    assert len(result3) == 0


def test_union_operator_with_invalid_keys():
    """Test union operator behavior with invalid range keys"""
    d = Dict()
    d[100:200] = "highlight"

    # Union with dict containing invalid keys should raise when processing
    invalid_dict = {"invalid_key": "value"}

    with pytest.raises(ValueError):
        d | invalid_dict

    with pytest.raises(ValueError):
        d |= invalid_dict


def test_equality_different_types():
    """Test equality with different types"""
    d = Dict()
    d[100:200] = "highlight"

    # Should not be equal to non-dict types
    assert d != "not a dict"
    assert d != 42
    assert d != [("100:200", "highlight")]
    assert d is not None


def test_hash_not_supported():
    """Test that Dict is not hashable (like regular dicts)"""
    d = Dict()
    d[100:200] = "highlight"

    # Dicts should not be hashable
    with pytest.raises(TypeError):
        hash(d)

    # Can't be used as dict keys
    container = {}
    with pytest.raises(TypeError):
        container[d] = "value"

    # Can't be added to sets
    with pytest.raises(TypeError):
        {d}
