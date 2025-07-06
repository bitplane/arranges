import pytest
from arranges import Segment


def test_union_with_empty_segment():
    """Test union when one segment is empty"""
    s1 = Segment(1, 5)
    s2 = Segment(0, 0)  # Empty segment

    # Union with empty should return the non-empty segment
    assert s1 | s2 == s1
    assert s2 | s1 == s1


def test_union_when_self_is_empty():
    """Test union when self is empty"""
    s1 = Segment(0, 0)  # Empty segment
    s2 = Segment(1, 5)

    assert s1 | s2 == s2


def test_union_with_non_connected_segments():
    """Test union with segments that aren't touching"""
    s1 = Segment(1, 5)
    s2 = Segment(10, 15)

    with pytest.raises(ValueError, match="1:5 and 10:15 aren't touching"):
        s1 | s2


def test_union_with_adjacent_segments():
    """Test union with adjacent segments"""
    s1 = Segment(1, 5)
    s2 = Segment(5, 10)

    assert s1 | s2 == Segment(1, 10)
    assert s2 | s1 == Segment(1, 10)


def test_union_with_overlapping_segments():
    """Test union with overlapping segments"""
    s1 = Segment(1, 7)
    s2 = Segment(5, 10)

    assert s1 | s2 == Segment(1, 10)
    assert s2 | s1 == Segment(1, 10)


def test_union_with_contained_segments():
    """Test union when one segment contains the other"""
    s1 = Segment(1, 10)
    s2 = Segment(3, 7)

    assert s1 | s2 == s1
    assert s2 | s1 == s1
