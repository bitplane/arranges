"""Test Dict update() behavior with overlaps and intersections"""

import pytest
from arranges import Dict


def test_update_with_dict():
    """Update with regular dict should work"""
    d = Dict()
    d[100:200] = "original"

    d.update({"300:400": "new"})

    assert d[100:200] == "original"
    assert d[300:400] == "new"
    assert len(d) == 2


def test_update_with_pairs():
    """Update with key-value pairs should work"""
    d = Dict()
    d[100:200] = "original"

    d.update([("300:400", "new"), ("500:600", "another")])

    assert d[100:200] == "original"
    assert d[300:400] == "new"
    assert d[500:600] == "another"
    assert len(d) == 3


def test_update_with_kwargs_only_valid_ranges():
    """Update with keyword arguments must be valid range strings"""
    d = Dict()
    d[100:200] = "original"

    # Only valid range strings work as kwargs
    with pytest.raises(ValueError, match="Invalid integer value"):
        d.update(key1="value1")  # Invalid range key

    # But valid range strings work as kwargs
    d.update(**{"300": "single_point"})  # Valid single position
    assert d[300] == "single_point"


def test_update_overlapping_ranges_replaces():
    """Update with overlapping ranges should replace like setitem"""
    d = Dict()
    d[100:300] = "original"

    # Update with overlapping range
    d.update({slice(200, 400): "new"})

    # Should split original and add new, just like setitem
    assert d[100:200] == "original"  # Remaining part
    assert d[200:400] == "new"  # New range
    assert len(d) == 2


def test_update_multiple_overlaps():
    """Update with multiple overlapping ranges"""
    d = Dict()
    d[100:200] = "first"
    d[300:400] = "second"
    d[500:600] = "third"

    # Update with ranges that overlap multiple existing
    d.update(
        {
            slice(150, 350): "overlap1",  # Overlaps first and second
            slice(550, 650): "overlap2",  # Overlaps third
        }
    )

    # Should handle all overlaps like multiple setitems
    assert d[100:150] == "first"  # Remaining part of first
    assert d[150:350] == "overlap1"  # New range
    assert d[350:400] == "second"  # Remaining part of second
    assert d[500:550] == "third"  # Remaining part of third
    assert d[550:650] == "overlap2"  # New range


def test_update_with_another_dict_instance():
    """Update with another Dict instance should work"""
    d1 = Dict()
    d1[100:200] = "first"

    d2 = Dict()
    d2[300:400] = "second"
    d2[200:300] = "middle"

    d1.update(d2)

    assert d1[100:200] == "first"
    assert d1[200:300] == "middle"
    assert d1[300:400] == "second"
    assert len(d1) == 3


def test_update_exact_key_replacement():
    """Update with exact same key should replace value"""
    d = Dict()
    d[100:200] = "original"

    d.update({"100:200": "replacement"})

    assert d[100:200] == "replacement"
    assert len(d) == 1


def test_update_adjacent_same_value_merge():
    """Update that creates adjacent same values should merge"""
    d = Dict()
    d[100:200] = "highlight"

    # Add adjacent range with same value
    d.update({slice(200, 300): "highlight"})

    # Should merge into single range
    assert d[100:300] == "highlight"
    assert len(d) == 1


def test_update_adjacent_different_values_no_merge():
    """Update that creates adjacent different values should not merge"""
    d = Dict()
    d[100:200] = "highlight"

    # Add adjacent range with different value
    d.update({slice(200, 300): "selection"})

    # Should remain separate
    assert d[100:200] == "highlight"
    assert d[200:300] == "selection"
    assert len(d) == 2


def test_update_with_none_values():
    """Update with None values should store None as valid values"""
    d = Dict()
    d[100:200] = "first"
    d[300:400] = "second"
    d[500:600] = "third"

    # Update with None as valid values
    d.update(
        {
            slice(150, 160): None,  # Assign None to part of first
            slice(300, 400): None,  # Assign None to all of second
        }
    )

    # Should have None values where assigned
    assert d[100:150] == "first"
    assert d[150:160] is None  # None value
    assert d[160:200] == "first"
    assert d[300:400] is None  # None value
    assert 155 in d and d[155] is None  # Has None value
    assert 350 in d and d[350] is None  # Has None value
    assert d[500:600] == "third"


def test_update_string_range_keys():
    """Update with string range keys should work"""
    d = Dict()
    d[100:200] = "original"

    d.update({"300:400": "new1", "1,3,5,7": "discrete"})

    assert d[300:400] == "new1"
    assert d["1,3,5,7"] == "discrete"
    assert 3 in d


def test_update_preserves_ranges_attribute():
    """Update should update the ranges attribute"""
    d = Dict()
    d[100:200] = "first"

    assert "100:200" in str(d.ranges)

    d.update({slice(300, 400): "second"})

    ranges_str = str(d.ranges)
    assert "100:200" in ranges_str
    assert "300:400" in ranges_str


def test_update_empty_dict():
    """Update with empty dict should not change anything"""
    d = Dict()
    d[100:200] = "original"

    d.update({})

    assert d[100:200] == "original"
    assert len(d) == 1


def test_update_order_matters():
    """Update order should matter for overlapping ranges"""
    d1 = Dict()
    d1[100:400] = "original"

    # Update with two overlapping ranges
    # The order they're processed matters
    updates = [
        (slice(200, 300), "first"),
        (slice(250, 350), "second"),  # Overlaps with first
    ]

    d1.update(updates)

    # Later update should win in overlap area
    assert d1[100:200] == "original"
    assert d1[200:250] == "first"
    assert d1[250:350] == "second"
    assert d1[350:400] == "original"


def test_update_with_integers():
    """Update with integer keys (single positions)"""
    d = Dict()
    d[100:200] = "range"

    d.update({300: "point1", 400: "point2"})

    assert d[100:200] == "range"
    assert d[300] == "point1"
    assert d[400] == "point2"
    assert 299 not in d
    assert 301 not in d


def test_update_complex_scenario():
    """Complex update scenario with multiple operations"""
    d = Dict()
    # Initial state
    d[100:200] = "A"
    d[300:400] = "B"
    d[500:600] = "C"

    # Complex update
    d.update(
        {
            slice(150, 350): "X",  # Overlaps A and B
            slice(450, 550): "Y",  # Overlaps C
            700: "Z",  # New single point
            slice(50, 75): "W",  # New range before everything
        }
    )

    # Check final state
    assert d[50:75] == "W"
    assert d[100:150] == "A"
    assert d[150:350] == "X"
    assert d[350:400] == "B"
    assert d[450:550] == "Y"
    assert d[550:600] == "C"
    assert d[700] == "Z"


def test_update_error_handling():
    """Update should handle argument errors like normal dict"""
    d = Dict()

    # Too many arguments should raise TypeError
    with pytest.raises(TypeError, match="update expected at most 1 argument, got 2"):
        d.update({slice(100, 200): "value1"}, {slice(300, 400): "value2"})

    # Single argument should work
    d.update({slice(100, 200): "value"})
    assert d[100:200] == "value"
