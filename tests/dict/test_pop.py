"""Test Dict pop() behavior - works like getitem (finds value) then removes"""

import pytest
from arranges import Dict, Ranges


def test_pop_exact_key():
    """Pop exact stored key should work like regular dict"""
    d = Dict()
    d[100:200] = "highlight"
    d[300:400] = "selection"

    value = d.pop("100:200")

    assert value == "highlight"
    assert "100:200" not in d
    assert d[300:400] == "selection"
    assert len(d) == 1


def test_pop_slice_exact_match():
    """Pop with slice that exactly matches stored key should work"""
    d = Dict()
    d[100:200] = "highlight"

    value = d.pop(slice(100, 200))

    assert value == "highlight"
    assert len(d) == 0


def test_pop_nonexistent_key_raises():
    """Pop non-existent exact key should raise KeyError"""
    d = Dict()
    d[100:200] = "highlight"

    with pytest.raises(KeyError):
        d.pop("300:400")  # Exact key that doesn't exist


def test_pop_nonexistent_key_with_default():
    """Pop non-existent key with default should return default"""
    d = Dict()
    d[100:200] = "highlight"

    result = d.pop("300:400", "default_value")

    assert result == "default_value"
    assert d[100:200] == "highlight"  # Unchanged


def test_pop_partial_range_contained():
    """Pop partial range should remove just that range (like get + del)"""
    d = Dict()
    d[100:300] = "highlight"

    # Partial range contained in single stored range returns that value
    value = d.pop(slice(150, 200))
    assert value == "highlight"

    # Should remove only the requested range, splitting the stored range
    assert 150 not in d  # Requested range removed
    assert 175 not in d  # Requested range removed
    assert 100 in d and d[100] == "highlight"  # Before split remains
    assert 250 in d and d[250] == "highlight"  # After split remains
    assert len(d) == 2  # 100:150, 200:300


def test_pop_single_position_works():
    """Pop single position should remove just that position (like get + del)"""
    d = Dict()
    d[100:200] = "highlight"
    d[300:400] = "selection"

    # Pop by position finds value and removes just that position
    value = d.pop(150)
    assert value == "highlight"

    # Should remove only position 150, splitting the range
    assert 150 not in d  # Position removed
    assert 100 in d and d[100] == "highlight"  # Range split: 100:150 remains
    assert 199 in d and d[199] == "highlight"  # Range split: 151:200 remains
    assert d[300:400] == "selection"  # Other range unchanged
    assert len(d) == 3  # 100:150, 151:200, 300:400


def test_pop_spanning_ranges_raises():
    """Pop range with gaps should raise KeyError"""
    d = Dict()
    d[100:200] = "highlight"
    d[300:400] = "selection"

    # Spans gaps - not fully contained
    with pytest.raises(KeyError):
        d.pop(slice(150, 350))


def test_pop_integer_key_exact_match():
    """Pop integer key that exactly matches stored key should work"""
    d = Dict()
    d[150] = "cursor"  # This stores as "150" (single position range)

    value = d.pop(150)

    assert value == "cursor"
    assert len(d) == 0


def test_pop_multi_segment_exact_match():
    """Pop multi-segment string that exactly matches should work"""
    d = Dict()
    d["100:200,300:400"] = "multi-selection"

    value = d.pop("100:200,300:400")

    assert value == "multi-selection"
    assert len(d) == 0


def test_pop_multi_segment_different_order_works():
    """Pop multi-segment with different order should work (logically equivalent)"""
    d = Dict()
    d["100:200,300:400"] = "multi-selection"

    # Different order but logically equivalent - should work
    value = d.pop("300:400,100:200")
    assert value == "multi-selection"
    assert len(d) == 0  # All ranges removed


def test_pop_empty_dict():
    """Pop from empty dict should raise KeyError"""
    d = Dict()

    with pytest.raises(KeyError):
        d.pop("100:200")

    # With default should return default
    result = d.pop("100:200", "default")
    assert result == "default"


def test_pop_updates_ranges():
    """Pop should update ranges attribute"""
    d = Dict()
    d[100:200] = "highlight"
    d[300:400] = "selection"

    original_ranges = str(d.ranges)
    assert "100:200" in original_ranges
    assert "300:400" in original_ranges

    d.pop("100:200")

    new_ranges = str(d.ranges)
    assert "100:200" not in new_ranges
    assert "300:400" in new_ranges


def test_pop_vs_del_same_behavior():
    """Demonstrate that pop and del have consistent behavior"""
    d1 = Dict()
    d1[100:300] = "highlight"

    d2 = Dict()
    d2[100:300] = "highlight"

    # del removes partial ranges (will split the range)
    del d1[150:200]  # Should split 100:300 into 100:150 and 200:300
    assert d1[100:150] == "highlight"
    assert d1[200:300] == "highlight"
    assert 175 not in d1

    # pop does the same: get + del = same result as del
    value = d2.pop(slice(150, 200))  # Same as get + del
    assert value == "highlight"
    assert d2[100:150] == "highlight"  # Same split as del
    assert d2[200:300] == "highlight"
    assert 175 not in d2
    assert len(d2) == 2  # Same result as del


def test_pop_with_ranges_as_key():
    """Pop with Ranges object as key"""
    d = Dict()
    d[Ranges("100:200,300:400")] = "multi-range"

    # Should work with same Ranges object
    value = d.pop(Ranges("100:200,300:400"))
    assert value == "multi-range"
    assert len(d) == 0


def test_popitem_still_works():
    """popitem() should work normally (removes arbitrary key-value pair)"""
    d = Dict()
    d[100:200] = "highlight"
    d[300:400] = "selection"

    key, value = d.popitem()

    # Should remove one of the pairs
    assert key in ["100:200", "300:400"]
    assert value in ["highlight", "selection"]
    assert len(d) == 1


def test_popitem_empty_dict():
    """popitem() on empty dict should raise KeyError like normal dict"""
    d = Dict()

    with pytest.raises(KeyError, match="popitem\\(\\): dictionary is empty"):
        d.popitem()
