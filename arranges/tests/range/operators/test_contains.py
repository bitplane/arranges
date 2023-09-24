import pytest

from arranges import Range


def test_contains_tuple():
    assert (1, 2, 3, 4, 5) in Range("1:6")


def test_doesnt_contain_sequence():
    assert (1, 2, 3, 5) not in Range("1:5")


def test_contains_range():
    assert Range("1:5") in Range("1:10")
    assert Range("2:10") in Range("2:")


def test_doesnt_contain_range():
    assert Range(":") not in Range("2:10")
    assert Range("1:10") not in Range("1:5")
    assert Range("2:") not in Range("2:10")


def test_nonetype_not_in_empty_range():
    assert None not in Range(None)


def test_nonetype_in_full_range():
    assert None in Range(":")


def test_nothing_in_empty():
    assert 1 not in Range("")
    assert [] not in Range(0, 0)
    assert Range("") not in Range("")


def test_contains_text_error():
    with pytest.raises(ValueError):
        "hello" in Range(":")


def test_contains_unsupported_type_error():
    class Crash:
        pass

    with pytest.raises(TypeError):
        Crash() in Range(":")


def test_contains_int():
    range = Range("1:10,20:30,100:150")

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


def test_contains_sequence():
    ranges = Range("1:10,20:30,100:150")

    assert range(10, 15) not in ranges
    assert range(100, 110) in ranges


def test_contains_ranges():
    ranges = Range("1:10,20:30,100:150")

    assert Range(20, 30) in ranges


def test_contains_empty_range():
    ranges = Range("1:10,20:30,100:150")
    empty = Range(0, 0)

    assert empty in ranges


def test_contains_broken():
    ranges = Range("1:10,20:30,100:150")

    assert [1, 3, 25, 125] in ranges
