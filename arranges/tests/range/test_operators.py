import pytest

from arranges import Range


def test_sort_order():
    """
    Sorted by start value only
    """
    assert not Range(":") < Range(":10")
    assert not Range(":10") < Range(":11")

    assert Range(":") < Range("1:")
    assert Range("5:") > Range("1:10")


def test_order_int():
    """
    Whichever comes first
    """
    # we can't do > here because that's an operator on the number object
    assert Range(100, 200) < 101
    assert not Range(0, 20) < -100


def test_equality_hash():
    assert hash(Range(":")) == hash(Range("0:inf"))
    assert hash(Range(":10")) == hash(Range("0:10"))
    assert hash(Range("10:")) != hash(Range("0:inf"))


def test_plus_operator():
    assert Range("1:10") + Range("5:15") == Range("1:15")
    assert Range(":10") + Range("9:") == Range(":")


def test_plus_operator_empty_range():
    expected = Range("1:10")
    empty = Range("0:0")

    actual_left = expected + empty
    actual_right = empty + expected

    assert actual_left == expected
    assert actual_right == expected


def test_plus_operator_non_overlapping():
    with pytest.raises(ValueError):
        Range("1:10") + Range("11:15")


def test_add_adjacent_ranges():
    assert Range("0:5") + Range("5:10") == Range("0:10")


def test_iterator():
    assert list(Range("1:10")) == [1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert list(Range("5")) == [0, 1, 2, 3, 4]
