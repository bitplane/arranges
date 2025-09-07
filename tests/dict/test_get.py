"""Test Dict __getitem__ intersection behavior"""

import pytest
from arranges import Dict


def test_exact_key_lookup():
    """Exact key match should return value"""
    d = Dict()
    d[100:200] = "highlight"

    assert d[100:200] == "highlight"
    assert d["100:200"] == "highlight"  # String form


def test_single_position_lookup():
    """Single position should find containing range"""
    d = Dict()
    d[100:200] = "highlight"
    d[300:400] = "selection"

    # Positions within ranges
    assert d[150] == "highlight"
    assert d[350] == "selection"

    # Boundary positions
    assert d[100] == "highlight"  # Start included
    assert d[199] == "highlight"  # End excluded, so 199 included
    assert d[300] == "selection"


def test_single_position_not_found():
    """Single position not in any range should raise KeyError"""
    d = Dict()
    d[100:200] = "highlight"
    d[300:400] = "selection"

    with pytest.raises(KeyError):
        d[99]  # Before first range

    with pytest.raises(KeyError):
        d[250]  # Gap between ranges

    with pytest.raises(KeyError):
        d[450]  # After last range


def test_partial_range_lookup_single_value():
    """Partial range contained in single stored range should return that value"""
    d = Dict()
    d[100:300] = "highlight"

    # Sub-ranges should return the containing value
    assert d[150:200] == "highlight"
    assert d[100:150] == "highlight"
    assert d[250:300] == "highlight"
    assert d[100:300] == "highlight"  # Exact match


def test_partial_range_lookup_not_contained():
    """Range not fully contained should raise KeyError"""
    d = Dict()
    d[100:200] = "highlight"
    d[300:400] = "selection"

    with pytest.raises(KeyError):
        d[150:250]  # Spans beyond highlight into gap

    with pytest.raises(KeyError):
        d[50:150]  # Starts before highlight

    with pytest.raises(KeyError):
        d[350:450]  # Extends beyond selection


def test_range_spanning_multiple_values_raises_error():
    """Range that spans multiple different values should raise ValueError"""
    d = Dict()
    d[100:200] = "highlight"
    d[200:300] = "selection"  # Different value, adjacent
    d[400:500] = "highlight"  # Same value as first, but not adjacent

    # Should raise ValueError for ranges spanning multiple different values
    with pytest.raises(ValueError):
        d[150:250]  # Spans highlight and selection (different values)

    with pytest.raises(KeyError):
        d[150:450]  # Spans ranges with gaps

    with pytest.raises(KeyError):
        d[100:500]  # Spans everything but has gaps


def test_range_spanning_gap_raises_error():
    """Range that includes gaps should raise KeyError or ValueError"""
    d = Dict()
    d[100:200] = "highlight"
    d[300:400] = "selection"

    # Range includes gap between stored ranges
    with pytest.raises((KeyError, ValueError)):
        d[150:350]  # Includes gap from 200:300


def test_range_with_identical_values_across_gap():
    """Range spanning identical values with gap should still raise error"""
    d = Dict()
    d[100:200] = "highlight"
    d[300:400] = "highlight"  # Same value but with gap

    # Even though values are the same, there's a gap
    with pytest.raises((KeyError, ValueError)):
        d[150:350]  # Spans across gap


def test_multi_segment_string_lookup():
    """Multi-segment string ranges should work"""
    d = Dict()
    d["100:200,300:400"] = "multi-selection"

    # Should find positions in any segment
    assert d[150] == "multi-selection"
    assert d[350] == "multi-selection"

    # Should work for sub-ranges within segments
    assert d[100:150] == "multi-selection"
    assert d[350:400] == "multi-selection"

    # Exact match should work
    assert d["100:200,300:400"] == "multi-selection"


def test_integer_key_lookup():
    """Integer keys (single positions) should work"""
    d = Dict()
    d[100] = "cursor"
    d[200] = "cursor"

    assert d[100] == "cursor"
    assert d[200] == "cursor"

    # Adjacent positions should not be included
    with pytest.raises(KeyError):
        d[99]
    with pytest.raises(KeyError):
        d[101]


def test_infinite_range_lookup():
    """Infinite ranges should work for lookups"""
    d = Dict()
    d[100:] = "tail-highlight"
    d[:50] = "head-highlight"

    assert d[100] == "tail-highlight"
    assert d[1000000] == "tail-highlight"
    assert d[0] == "head-highlight"
    assert d[49] == "head-highlight"

    # Should work for sub-ranges
    assert d[200:300] == "tail-highlight"
    assert d[0:25] == "head-highlight"


def test_empty_range_lookup():
    """Empty ranges should not match anything"""
    d = Dict()
    d[100:200] = "highlight"

    # Empty range lookups should raise KeyError
    with pytest.raises(KeyError):
        d[150:150]  # Empty range

    with pytest.raises(KeyError):
        d[""]  # Empty string range


def test_boundary_conditions():
    """Test exact boundary conditions"""
    d = Dict()
    d[100:200] = "highlight"

    # Start boundary included
    assert d[100] == "highlight"

    # End boundary excluded
    with pytest.raises(KeyError):
        d[200]  # Should not be included

    # Just before end should be included
    assert d[199] == "highlight"


def test_overlapping_ranges_last_wins():
    """When ranges overlap, later assignment should win for lookups"""
    d = Dict()
    d[100:300] = "original"
    d[200:400] = "override"  # Overlaps 200:300

    # This test assumes setitem handles overlaps correctly
    # The behavior depends on how setitem resolves conflicts
    # This test documents expected lookup behavior after conflicts resolved


def test_get_method_with_intersection():
    """get() method should use same intersection logic"""
    d = Dict()
    d[100:200] = "highlight"

    # Should find intersecting values
    assert d.get(150) == "highlight"
    assert d.get(99) is None
    assert d.get(99, "default") == "default"

    # Should work with ranges too
    assert d.get(slice(100, 150)) == "highlight"
    assert d.get(slice(50, 75)) is None
