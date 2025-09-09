from arranges import Ranges


def test_contains_tuple():
    assert (1, 2, 3, 4, 5) in Ranges("1:6")


def test_doesnt_contain_sequence():
    assert (1, 2, 3, 5) not in Ranges("1:5")


def test_contains_range():
    assert Ranges("1:5") in Ranges("1:10")
    assert Ranges("2:10") in Ranges("2:")


def test_doesnt_contain_range():
    assert Ranges(":") not in Ranges("2:10")
    assert Ranges("1:10") not in Ranges("1:5")
    assert Ranges("2:") not in Ranges("2:10")


def test_nonetype_not_in_empty_range():
    assert None not in Ranges(None)


def test_nonetype_in_full_range():
    assert None in Ranges(":")


def test_nothing_in_empty():
    assert 1 not in Ranges("")
    assert [] not in Ranges(0, 0)
    assert Ranges("") not in Ranges("")


def test_contains_invalid_text():
    """Text that isn't a valid range should return False, not raise."""
    assert "hello" not in Ranges(":")
    assert "world" not in Ranges("1:10")


def test_contains_unsupported_type():
    """Unsupported types should return False, not raise."""

    class Crash:
        pass

    assert Crash() not in Ranges(":")
    assert Crash() not in Ranges("1:10")


def test_contains_int():
    range = Ranges("1:10,20:30,100:150")

    assert 0 not in range
    assert 1 in range
    assert 5 in range
    assert 10 not in range
    assert 19 not in range
    assert 20 in range
    assert 30 not in range
    assert 100 in range
    assert 149 in range
    assert 150 not in range


def test_negative_integers_not_contained():
    """Negative integers should not raise; simply return False."""
    assert -1 not in Ranges(10)
    assert -100 not in Ranges(":")


def test_invalid_string_not_contained():
    """Invalid range strings should return False or raise appropriately."""
    assert "not a range" not in Ranges(0, 10)
    assert "hello world" not in Ranges("1:10")


def test_contains_sequence():
    ranges = Ranges("1:10,20:30,100:150")

    assert range(10, 15) not in ranges
    assert range(100, 110) in ranges


def test_contains_ranges():
    ranges = Ranges("1:10,20:30,100:150")

    assert Ranges(20, 30) in ranges


def test_contains_empty_range():
    ranges = Ranges("1:10,20:30,100:150")
    empty = Ranges(0, 0)

    assert empty in ranges


def test_contains_split_range():
    ranges = Ranges("1:10,20:30,100:150")

    assert [1, 3, 25, 125] in ranges
