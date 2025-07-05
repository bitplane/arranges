from arranges.segment import Segment


def test_less_than():
    assert Segment(1, 5) < Segment(6, 10)
    assert Segment(1, 5) < Segment(2, 6)
    assert not (Segment(2, 6) < Segment(1, 5))
    assert not (Segment(1, 5) < Segment(1, 5))

    # Test with overlap
    assert Segment(1, 3) < Segment(2, 5)
    assert not (Segment(2, 5) < Segment(1, 3))


def test_less_than_or_equal():
    assert Segment(1, 5) <= Segment(6, 10)
    assert Segment(1, 5) <= Segment(2, 6)
    assert Segment(1, 5) <= Segment(1, 5)
    assert not (Segment(2, 6) <= Segment(1, 5))


def test_greater_than():
    assert Segment(6, 10) > Segment(1, 5)
    assert Segment(2, 6) > Segment(1, 5)
    assert not (Segment(1, 5) > Segment(2, 6))
    assert not (Segment(1, 5) > Segment(1, 5))

    # Test with overlap
    assert Segment(2, 5) > Segment(1, 3)
    assert not (Segment(1, 3) > Segment(2, 5))


def test_greater_than_or_equal():
    assert Segment(6, 10) >= Segment(1, 5)
    assert Segment(2, 6) >= Segment(1, 5)
    assert Segment(1, 5) >= Segment(1, 5)
    assert not (Segment(1, 5) >= Segment(2, 6))


def test_comparison_with_infinite_segments():
    from arranges.utils import inf

    # Infinite segments should be greater than finite ones
    assert Segment(0, inf) > Segment(0, 100)
    assert Segment(0, inf) >= Segment(0, 100)
    assert Segment(0, 100) < Segment(0, inf)
    assert Segment(0, 100) <= Segment(0, inf)

    # Equal infinite segments
    assert Segment(0, inf) <= Segment(0, inf)
    assert Segment(0, inf) >= Segment(0, inf)
    assert not (Segment(0, inf) < Segment(0, inf))
    assert not (Segment(0, inf) > Segment(0, inf))


def test_comparison_edge_cases():
    # Empty segments
    assert Segment(5, 5) < Segment(6, 6)
    assert Segment(5, 5) <= Segment(5, 5)

    # Adjacent segments
    assert Segment(1, 5) < Segment(5, 10)
    assert Segment(5, 10) > Segment(1, 5)
