"""Test Dict __delitem__ behavior with range deletions and intersections"""

import pytest
from arranges import Dict


def test_exact_key_deletion():
    """Delete exact stored key"""
    d = Dict()
    d[100:200] = "highlight"
    d[300:400] = "selection"

    del d["100:200"]  # Delete by exact key string

    assert "100:200" not in d
    assert d[300:400] == "selection"
    assert len(d) == 1
    assert 150 not in d


def test_slice_key_deletion():
    """Delete using slice syntax"""
    d = Dict()
    d[100:200] = "highlight"
    d[300:400] = "selection"

    del d[100:200]  # Delete by slice

    assert 150 not in d
    assert d[300:400] == "selection"
    assert len(d) == 1


def test_partial_range_deletion_front():
    """Delete front part of a range"""
    d = Dict()
    d[100:300] = "highlight"

    del d[100:200]  # Delete front part

    # Should leave back part
    assert d[200:300] == "highlight"
    assert len(d) == 1
    assert 150 not in d  # Deleted part
    assert 250 in d  # Remaining part


def test_partial_range_deletion_back():
    """Delete back part of a range"""
    d = Dict()
    d[100:300] = "highlight"

    del d[200:300]  # Delete back part

    # Should leave front part
    assert d[100:200] == "highlight"
    assert len(d) == 1
    assert 250 not in d  # Deleted part
    assert 150 in d  # Remaining part


def test_partial_range_deletion_middle():
    """Delete middle part of a range"""
    d = Dict()
    d[100:400] = "highlight"

    del d[200:300]  # Delete middle part

    # Should split into two ranges
    assert d[100:200] == "highlight"
    assert d[300:400] == "highlight"
    assert len(d) == 2
    assert 250 not in d  # Deleted part
    assert 150 in d  # First remaining part
    assert 350 in d  # Second remaining part


def test_delete_spanning_multiple_ranges():
    """Delete range that spans multiple stored ranges"""
    d = Dict()
    d[100:150] = "first"
    d[200:250] = "second"
    d[300:350] = "third"

    del d[125:325]  # Spans across all three with gaps

    # Should remove overlapped parts
    assert d[100:125] == "first"  # Remaining part of first
    assert d[325:350] == "third"  # Remaining part of third
    assert len(d) == 2

    # Check deletions
    assert 140 not in d  # Was in first range
    assert 225 not in d  # Was in second range
    assert 310 not in d  # Was in third range


def test_delete_complete_overlap():
    """Delete range that completely contains stored ranges"""
    d = Dict()
    d[150:175] = "small"
    d[200:225] = "also-small"

    del d[100:300]  # Completely contains both

    # Should delete both ranges completely
    assert len(d) == 0
    assert 160 not in d
    assert 210 not in d


def test_delete_nonexistent_exact_key():
    """Delete non-existent exact key should raise KeyError"""
    d = Dict()
    d[100:200] = "highlight"

    with pytest.raises(KeyError):
        del d["300:400"]  # Exact key that doesn't exist


def test_delete_nonexistent_range_key():
    """Delete non-existent range should raise KeyError"""
    d = Dict()
    d[100:200] = "highlight"

    # Non-intersecting ranges should raise KeyError like normal dicts
    with pytest.raises(KeyError):
        del d[300:400]  # Range that doesn't intersect


def test_delete_partial_nonexistent():
    """Delete range that partially doesn't exist"""
    d = Dict()
    d[200:300] = "highlight"

    del d[150:250]  # Partially overlaps 200:250

    # Should only affect the overlapping part
    assert d[250:300] == "highlight"
    assert len(d) == 1
    assert 225 not in d  # Deleted part
    assert 275 in d  # Remaining part


def test_delete_integer_key():
    """Delete single position"""
    d = Dict()
    d[100:200] = "highlight"

    del d[150]  # Delete single position

    # Should split the range
    assert d[100:150] == "highlight"
    assert d[151:200] == "highlight"
    assert len(d) == 2
    assert 150 not in d


def test_delete_string_range_key():
    """Delete using string range syntax"""
    d = Dict()
    d[100:300] = "highlight"

    del d["150:250"]  # String range key

    # Should split the range
    assert d[100:150] == "highlight"
    assert d[250:300] == "highlight"
    assert len(d) == 2


def test_delete_multi_segment_string():
    """Delete using multi-segment string range"""
    d = Dict()
    d[100:400] = "highlight"

    del d["150:200,250:300"]  # Multi-segment deletion

    # Should create multiple splits
    assert d[100:150] == "highlight"
    assert d[200:250] == "highlight"
    assert d[300:400] == "highlight"
    assert len(d) == 3

    # Check deletions
    assert 175 not in d  # First deleted segment
    assert 275 not in d  # Second deleted segment


def test_delete_affects_ranges_attribute():
    """Deletion should update the ranges attribute"""
    d = Dict()
    d[100:200] = "highlight"
    d[300:400] = "selection"

    original_ranges = str(d.ranges)
    assert "100:200" in original_ranges
    assert "300:400" in original_ranges

    del d[100:200]

    new_ranges = str(d.ranges)
    assert "100:200" not in new_ranges
    assert "300:400" in new_ranges


def test_delete_beyond_stored_ranges_silent():
    """Delete can extend beyond stored ranges without error"""
    d = Dict()
    d[200:300] = "highlight"

    # Delete range that extends beyond stored data should work
    del d[100:400]  # Completely contains 200:300 plus extra

    # Should delete the contained range
    assert len(d) == 0
    assert 250 not in d


def test_delete_empty_intersection_raises():
    """Delete with no intersection should raise KeyError"""
    d = Dict()
    d[100:200] = "highlight"

    # Delete range that doesn't intersect should raise KeyError
    with pytest.raises(KeyError):
        del d[300:400]  # No intersection

    # Should not affect existing data
    assert d[100:200] == "highlight"
    assert len(d) == 1


def test_delete_all_with_infinite_range():
    """Should be able to delete everything with infinite range"""
    d = Dict()
    d[100:200] = "first"
    d[300:400] = "second"
    d[500:600] = "third"

    # Delete everything
    del d[:]

    # Should be empty
    assert len(d) == 0
    assert d.ranges == ""
