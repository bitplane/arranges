from arranges import Segment, Ranges


def test_equality_with_empty_segments():
    """Test equality when both segments are empty"""
    s1 = Segment(0, 0)
    s2 = Segment(0, 0)

    assert s1 == s2
    assert s2 == s1

    # Empty segment equals None
    assert s1 == None  # noqa: E711
    assert None == s1  # noqa: E711


def test_equality_with_ranges():
    """Test equality with Ranges objects"""
    s = Segment(5, 10)

    # Single-segment Ranges
    r1 = Ranges("5:10")
    assert s == r1
    assert r1 == s

    # Multi-segment Ranges
    r2 = Ranges("1:3,5:10")
    assert s != r2
    assert r2 != s

    # Empty Ranges
    r3 = Ranges("")
    empty_s = Segment(0, 0)
    assert empty_s == r3
    assert r3 == empty_s


def test_equality_after_coercion():
    """Test equality with objects that get coerced"""
    s = Segment(5, 10)

    # Range object
    assert s == range(5, 10)
    assert range(5, 10) == s

    # List (should not be equal as it's not coercible to a matching segment)
    assert s != [5, 6, 7, 8, 9]

    # Object that can't be coerced
    assert s != {"not": "a segment"}
    assert {"not": "a segment"} != s


def test_equality_edge_cases():
    """Test various edge cases for equality"""
    s = Segment(5, 10)

    # Same segment
    assert s == s

    # Different segments
    assert s != Segment(5, 11)
    assert s != Segment(4, 10)

    # Single value segments
    s1 = Segment(5, 6)
    s2 = Segment(5, 6)
    assert s1 == s2


def test_equality_with_integer():
    """Test equality with integers"""
    # Single-value segment equals integer
    assert Segment(5, 6) == 5
    assert 5 == Segment(5, 6)

    # Multi-value segment does not equal integer
    assert Segment(5, 10) != 5
    assert 5 != Segment(5, 10)


def test_equality_with_string():
    """Test equality with strings"""
    assert Segment(5, 10) == "5:10"
    assert "5:10" == Segment(5, 10)

    assert Segment(5, 6) == "5"
    assert "5" == Segment(5, 6)

    assert Segment(5, 10) != "5:11"
    assert "5:11" != Segment(5, 10)


def test_equality_with_unconvertible_objects():
    """Test equality with objects that can't be coerced"""
    s = Segment(5, 10)

    # Objects that can't be converted to Segment should return False
    assert s != object()
    assert s != {"not": "convertible"}

    # Function objects can't be converted to Segment
    def func(x):
        return x

    assert s != func

    # Custom class that won't be converted
    class UnconvertibleClass:
        pass

    obj = UnconvertibleClass()
    assert s != obj  # Should hit the return False line
