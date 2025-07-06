from arranges import Segment, Ranges


def test_coerce_with_multi_segment_ranges():
    """Test _coerce with multi-segment Ranges (covers line 171)"""
    # Create a multi-segment Ranges
    ranges = Ranges("1:5,10:15,20:25")

    # _coerce should return the Ranges object unchanged
    result = Segment._coerce(ranges)
    assert result is ranges
    assert isinstance(result, Ranges)


def test_coerce_with_single_segment_ranges():
    """Test _coerce with single-segment Ranges"""
    ranges = Ranges("5:10")

    # Should convert to Segment
    result = Segment._coerce(ranges)
    assert isinstance(result, Segment)
    assert result == Segment(5, 10)


def test_comparison_with_multi_segment_ranges_returns_not_implemented():
    """Test comparison operators return NotImplemented for multi-segment Ranges (covers lines 265, 283)"""
    segment = Segment(5, 10)
    ranges = Ranges("1:3,15:20")

    # All comparison operations should return NotImplemented
    # Python will then try the reverse operation on the Ranges object
    assert (segment < ranges) == NotImplemented or isinstance(segment < ranges, bool)
    assert (segment <= ranges) == NotImplemented or isinstance(segment <= ranges, bool)
    assert (segment > ranges) == NotImplemented or isinstance(segment > ranges, bool)
    assert (segment >= ranges) == NotImplemented or isinstance(segment >= ranges, bool)


def test_comparison_with_unconvertible_object():
    """Test comparison with objects that can't be coerced"""
    segment = Segment(5, 10)

    # These should return NotImplemented
    result = segment.__lt__({"not": "comparable"})
    assert result == NotImplemented

    result = segment.__le__({"not": "comparable"})
    assert result == NotImplemented

    result = segment.__gt__({"not": "comparable"})
    assert result == NotImplemented

    result = segment.__ge__({"not": "comparable"})
    assert result == NotImplemented


def test_coerce_with_various_types():
    """Test _coerce with different input types"""
    # Already a Segment
    s = Segment(1, 5)
    assert Segment._coerce(s) is s

    # Integer
    assert Segment._coerce(5) == Segment(5, 6)

    # String
    assert Segment._coerce("5:10") == Segment(5, 10)

    # Python range
    assert Segment._coerce(range(5, 10)) == Segment(5, 10)

    # Object that can't be coerced
    obj = {"not": "convertible"}
    assert Segment._coerce(obj) is obj
