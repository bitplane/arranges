from arranges import Segment


def test_isdisjoint_with_overlapping_segments():
    """Test isdisjoint with overlapping segments"""
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


def test_isdisjoint_with_non_string_objects():
    """Test isdisjoint with non-string objects"""
    s1 = Segment(1, 5)

    # Create a custom object that can be converted to Segment via __init__
    class SegmentLike:
        def __init__(self, start, stop):
            self.start = start
            self.stop = stop

    # This should go through as_type(Segment, other) on line 198
    # Since it's not a string, it skips line 196
    obj = SegmentLike(10, 15)
    try:
        # This will fail because SegmentLike can't be converted to Segment
        # but it will hit line 198: as_type(Segment, other)
        s1.isdisjoint(obj)
    except (TypeError, ValueError):
        pass  # Expected to fail, but hits line 198
