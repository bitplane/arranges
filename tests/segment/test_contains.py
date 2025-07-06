import pytest
from arranges import Segment


def test_contains_with_empty_segment():
    """Test __contains__ with empty segment (covers line 293)"""
    empty = Segment(0, 0)

    # Nothing is contained in an empty segment
    assert 5 not in empty
    assert "5" not in empty
    assert [1, 2, 3] not in empty
    assert Segment(1, 5) not in empty
    assert range(1, 5) not in empty


def test_contains_with_string():
    """Test __contains__ with string arguments (covers lines 305-306)"""
    s = Segment(5, 15)

    # String representing a segment within
    assert "7:10" in s
    assert "5:15" in s

    # String representing a segment outside
    assert "1:3" not in s
    assert "20:25" not in s

    # String representing a segment partially overlapping
    assert "10:20" not in s

    # Single value strings
    assert "7" in s
    assert "20" not in s


def test_contains_with_iterable():
    """Test __contains__ with iterable arguments (covers lines 308-312)"""
    s = Segment(5, 15)

    # List of values all within
    assert [5, 7, 10, 14] in s

    # List with some values outside
    assert [5, 7, 20] not in s

    # Empty list is contained in any segment
    assert [] in s

    # Tuple
    assert (7, 8, 9) in s

    # Set
    assert {6, 7, 8} in s
    assert {6, 7, 20} not in s

    # Generator
    assert (x for x in range(7, 10)) in s


def test_contains_with_unsupported_type():
    """Test __contains__ with unsupported types (covers line 314)"""
    s = Segment(5, 15)

    # Non-iterable object should raise TypeError
    with pytest.raises(TypeError, match="Unsupported type"):
        object() in s


def test_contains_with_integers():
    """Test __contains__ with integer values"""
    s = Segment(5, 15)

    assert 5 in s
    assert 10 in s
    assert 14 in s
    assert 15 not in s  # End is exclusive
    assert 4 not in s
    assert 20 not in s


def test_contains_with_range_objects():
    """Test __contains__ with Python range objects"""
    s = Segment(5, 20)

    # Range completely within
    assert range(7, 15) in s
    assert range(5, 20) in s

    # Range partially outside
    assert range(3, 10) not in s
    assert range(15, 25) not in s

    # Empty range
    assert range(0, 0) in s
    assert range(10, 10) in s


def test_contains_with_segments():
    """Test __contains__ with other Segment objects"""
    s = Segment(5, 20)

    # Segment completely within
    assert Segment(7, 15) in s
    assert Segment(5, 20) in s

    # Segment partially outside
    assert Segment(3, 10) not in s
    assert Segment(15, 25) not in s

    # Empty segment
    assert Segment(0, 0) in s
