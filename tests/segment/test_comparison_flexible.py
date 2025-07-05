from arranges.segment import Segment
from arranges import Ranges


def test_comparison_with_ranges():
    """Test comparing Segment with Ranges objects"""
    # Segment should be comparable with single-segment Ranges
    assert Segment(1, 5) < Ranges("6:10")
    assert Segment(6, 10) > Ranges("1:5")
    assert Segment(1, 5) <= Ranges("1:5")
    assert Segment(1, 5) >= Ranges("1:5")


def test_comparison_with_strings():
    """Test comparing Segment with string representations"""
    assert Segment(1, 5) < "6:10"
    assert Segment(6, 10) > "1:5"
    assert Segment(1, 5) <= "1:5"
    assert Segment(1, 5) >= "1:5"


def test_comparison_with_integers():
    """Test comparing Segment with integers (single values)"""
    # Integer 5 means range [5:6)
    assert Segment(1, 5) < 5
    assert Segment(6, 10) > 5
    assert Segment(5, 6) <= 5
    assert Segment(5, 6) >= 5


def test_comparison_with_range_objects():
    """Test comparing Segment with Python range objects"""
    assert Segment(1, 5) < range(6, 10)
    assert Segment(6, 10) > range(1, 5)
    assert Segment(1, 5) <= range(1, 5)
    assert Segment(1, 5) >= range(1, 5)


def test_comparison_fails_gracefully():
    """Test that comparison with incompatible types returns False or raises TypeError"""
    import pytest

    # These should raise TypeError
    with pytest.raises(TypeError):
        Segment(1, 5) < {"not": "comparable"}

    with pytest.raises(TypeError):
        Segment(1, 5) > [1, 2, 3]
