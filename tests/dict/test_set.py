"""Test Dict __setitem__ behavior with overlaps and intersections"""

import pytest
from arranges import Dict


def test_basic_setitem():
    """Basic setitem with no overlaps"""
    d = Dict()
    d[100:200] = "highlight"
    assert d[100:200] == "highlight"
    assert len(d) == 1


def test_exact_overwrite():
    """Setting same range twice should overwrite"""
    d = Dict()
    d[100:200] = "highlight"
    d[100:200] = "selection"  # Same range
    assert d[100:200] == "selection"
    assert len(d) == 1


def test_non_overlapping_ranges():
    """Non-overlapping ranges should coexist"""
    d = Dict()
    d[100:200] = "highlight"
    d[300:400] = "selection"
    assert d[100:200] == "highlight"
    assert d[300:400] == "selection"
    assert len(d) == 2


def test_complete_overlap_replacement():
    """New range completely contains existing range"""
    d = Dict()
    d[150:175] = "small-highlight"
    d[100:200] = "big-highlight"  # Contains 150:175

    # Should replace the smaller range
    assert d[100:200] == "big-highlight"
    assert 160 in d
    assert d[160] == "big-highlight"
    # Should only have one segment
    assert len(d) == 1


def test_partial_overlap_front():
    """New range overlaps front of existing range"""
    d = Dict()
    d[150:250] = "original"
    d[100:200] = "new"  # Overlaps 150:200 of original

    # Should split the original range
    assert d[100:200] == "new"  # New range
    assert d[200:250] == "original"  # Remaining part of original
    assert len(d) == 2

    # Boundary checks
    assert 175 in d and d[175] == "new"
    assert 225 in d and d[225] == "original"
    assert 125 in d and d[125] == "new"  # 125 is covered by 100:200 range


def test_partial_overlap_back():
    """New range overlaps back of existing range"""
    d = Dict()
    d[100:200] = "original"
    d[150:250] = "new"  # Overlaps 150:200 of original

    # Should split the original range
    assert d[100:150] == "original"  # Remaining part of original
    assert d[150:250] == "new"  # New range
    assert len(d) == 2

    # Boundary checks
    assert 125 in d and d[125] == "original"
    assert 200 in d and d[200] == "new"


def test_middle_overlap():
    """New range overlaps middle of existing range"""
    d = Dict()
    d[100:300] = "original"
    d[150:250] = "new"  # Overlaps middle 150:250

    # Should split original into two parts
    assert d[100:150] == "original"  # Before overlap
    assert d[150:250] == "new"  # Overlap area
    assert d[250:300] == "original"  # After overlap
    assert len(d) == 3

    # Boundary checks
    assert 125 in d and d[125] == "original"
    assert 200 in d and d[200] == "new"
    assert 275 in d and d[275] == "original"


def test_multiple_range_overlap():
    """New range overlaps multiple existing ranges"""
    d = Dict()
    d[100:150] = "first"
    d[200:250] = "second"
    d[300:350] = "third"
    d[125:325] = "new"  # Overlaps all three

    # Should replace overlapped parts
    assert d[100:125] == "first"  # Remaining part of first
    assert d[125:325] == "new"  # New range (replaces middle parts)
    assert d[325:350] == "third"  # Remaining part of third
    assert len(d) == 3

    # Check that middle range is completely gone
    assert 225 in d and d[225] == "new"  # Was in "second" range


def test_adjacent_same_value_merge():
    """Adjacent ranges with same value should merge"""
    d = Dict()
    d[100:200] = "highlight"
    d[200:300] = "highlight"  # Adjacent, same value

    # Should merge into single range
    assert d[100:300] == "highlight"
    assert len(d) == 1

    # Should work across the boundary
    assert 150 in d and d[150] == "highlight"
    assert 250 in d and d[250] == "highlight"


def test_adjacent_different_value_no_merge():
    """Adjacent ranges with different values should not merge"""
    d = Dict()
    d[100:200] = "highlight"
    d[200:300] = "selection"  # Adjacent, different value

    # Should remain separate
    assert d[100:200] == "highlight"
    assert d[200:300] == "selection"
    assert len(d) == 2


def test_none_assignment_valid():
    """Assigning None should store None as a valid value"""
    d = Dict()
    d[100:300] = "highlight"
    d[150:200] = None  # Assign None as value

    # Should split into three ranges
    assert d[100:150] == "highlight"
    assert d[150:200] is None  # None is a valid value
    assert d[200:300] == "highlight"
    assert 175 in d  # Has value None
    assert len(d) == 3


def test_string_range_keys():
    """String range keys should work"""
    d = Dict()
    d["100:200"] = "highlight"
    d["1,3,5,7"] = "discrete"  # Multi-segment range

    assert d["100:200"] == "highlight"
    assert d["1,3,5,7"] == "discrete"
    assert 150 in d
    assert 3 in d


def test_integer_keys():
    """Integer keys should work as single positions"""
    d = Dict()
    d[100] = "cursor"
    d[200] = "cursor"

    assert d[100] == "cursor"
    assert d[200] == "cursor"
    assert 99 not in d
    assert 101 not in d


def test_slice_step_rejection():
    """Slice with step should raise error"""
    d = Dict()
    with pytest.raises(ValueError, match="Stepped ranges not supported"):
        d[0:100:2] = "invalid"


def test_negative_ranges_rejection():
    """Negative ranges should raise error"""
    d = Dict()
    with pytest.raises(ValueError):
        d[-10:10] = "invalid"
