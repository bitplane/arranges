from arranges import Segment


def test_isdisjoint_with_overlapping_segments():
    """Test isdisjoint with overlapping segments (covers lines 195-196)"""
    s1 = Segment(1, 10)
    s2 = Segment(5, 15)

    assert not s1.isdisjoint(s2)
    assert not s2.isdisjoint(s1)


def test_isdisjoint_with_adjacent_segments():
    """Test isdisjoint with adjacent segments"""
    s1 = Segment(1, 5)
    s2 = Segment(5, 10)

    # Adjacent segments ARE disjoint (they don't overlap, just touch)
    assert s1.isdisjoint(s2)
    assert s2.isdisjoint(s1)


def test_isdisjoint_with_separate_segments():
    """Test isdisjoint with completely separate segments"""
    s1 = Segment(1, 5)
    s2 = Segment(10, 15)

    assert s1.isdisjoint(s2)
    assert s2.isdisjoint(s1)


def test_isdisjoint_with_contained_segments():
    """Test isdisjoint when one segment contains the other"""
    s1 = Segment(1, 20)
    s2 = Segment(5, 10)

    assert not s1.isdisjoint(s2)
    assert not s2.isdisjoint(s1)


def test_isdisjoint_with_string():
    """Test isdisjoint with string argument"""
    s1 = Segment(1, 5)

    assert s1.isdisjoint("10:15")
    assert not s1.isdisjoint("3:7")


def test_isdisjoint_with_empty_segments():
    """Test isdisjoint with empty segments"""
    s1 = Segment(1, 5)
    s2 = Segment(0, 0)  # Empty

    # Empty segments are considered to intersect with everything
    assert not s1.isdisjoint(s2)
    assert not s2.isdisjoint(s1)

    # Two empty segments are disjoint
    s3 = Segment(0, 0)
    assert s2.isdisjoint(s3)
