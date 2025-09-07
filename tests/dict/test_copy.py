"""Test Dict copy behavior and independence"""

from arranges import Dict


def test_basic_copy():
    """Basic copy should work"""
    d1 = Dict()
    d1[100:200] = "highlight"
    d1[300:400] = "selection"

    d2 = d1.copy()

    # Should have same contents
    assert d2[100:200] == "highlight"
    assert d2[300:400] == "selection"
    assert len(d2) == 2

    # Should be different objects
    assert d2 is not d1
    assert d2.ranges is not d1.ranges


def test_copy_independence_values():
    """Modifying copied dict should not affect original"""
    d1 = Dict()
    d1[100:200] = "original"

    d2 = d1.copy()
    d2[100:200] = "modified"

    # Original should be unchanged
    assert d1[100:200] == "original"
    assert d2[100:200] == "modified"


def test_copy_independence_structure():
    """Adding/removing ranges in copy should not affect original"""
    d1 = Dict()
    d1[100:200] = "highlight"

    d2 = d1.copy()
    d2[300:400] = "new-range"
    del d2[100:200]

    # Original should be unchanged
    assert d1[100:200] == "highlight"
    assert 300 not in d1
    assert len(d1) == 1

    # Copy should be different
    assert 100 not in d2
    assert d2[300:400] == "new-range"
    assert len(d2) == 1


def test_copy_ranges_independence():
    """ranges attribute should be independent in copies"""
    d1 = Dict()
    d1[100:200] = "highlight"

    d2 = d1.copy()

    # Should have same ranges initially
    assert str(d1.ranges) == str(d2.ranges)

    # Modifying one should not affect the other's ranges
    d2[300:400] = "new"

    assert "300:400" in str(d2.ranges)
    assert "300:400" not in str(d1.ranges)


def test_copy_empty_dict():
    """Copying empty dict should work"""
    d1 = Dict()
    d2 = d1.copy()

    assert len(d2) == 0
    assert d2.ranges == ""
    assert d2 is not d1


def test_copy_with_complex_ranges():
    """Copy should handle complex multi-segment ranges"""
    d1 = Dict()
    d1["100:200,300:400"] = "multi-segment"
    d1[500] = "single-point"
    d1[:1000] = "infinite-start"  # This overwrites the overlapping ranges

    d2 = d1.copy()

    # After infinite-start overwrites, ranges 100:200,300:400 are now infinite-start
    assert d2["100:200,300:400"] == "infinite-start"
    assert d2[500] == "infinite-start"  # This was also overwritten
    assert d2[:1000] == "infinite-start"

    # Should work for containment
    assert 150 in d2
    assert 350 in d2
    assert 500 in d2
    assert 50 in d2  # Part of :1000


def test_copy_preserves_dict_interface():
    """Copy should preserve all dict interface methods"""
    d1 = Dict()
    d1[100:200] = "highlight"
    d1[300:400] = "selection"

    d2 = d1.copy()

    # Should support all dict operations
    assert list(d2.keys()) == list(d1.keys())
    assert list(d2.values()) == list(d1.values())
    assert list(d2.items()) == list(d1.items())

    # Should support dict methods
    assert d2.get("100:200") == "highlight"
    assert d2.get("500:600") is None  # Valid range, just not stored

    d2.update({"500:600": "new"})
    assert d2["500:600"] == "new"
    assert "500:600" not in d1  # Independence


def test_deepcopy_mutable_values():
    """Copy with mutable values should work correctly"""
    d1 = Dict()
    d1[100:200] = {"type": "highlight", "color": "yellow"}
    d1[300:400] = ["item1", "item2"]

    d2 = d1.copy()

    # Should have same values initially
    assert d2[100:200] == {"type": "highlight", "color": "yellow"}
    assert d2[300:400] == ["item1", "item2"]

    # Note: dict.copy() is shallow, so mutable values are shared
    # This is standard dict behavior, but we should document it
    d2[100:200]["color"] = "blue"  # Modifies shared dict
    assert d1[100:200]["color"] == "blue"  # Also changed in original

    # But the ranges themselves are independent
    d2[100:200] = {"completely": "different"}
    assert d1[100:200]["color"] == "blue"  # Original value unchanged


def test_copy_from_constructor():
    """Dict constructor copy should work like dict.copy()"""
    d1 = Dict()
    d1[100:200] = "highlight"

    d2 = Dict(d1)  # Constructor copy

    assert d2[100:200] == "highlight"
    assert d2 is not d1

    # Should be independent
    d2[300:400] = "new"
    assert 300 not in d1
