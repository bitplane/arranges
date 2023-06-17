import pytest

from arranges import Range


def test_contains_int():
    assert 1 in Range("1:10")
    assert 9 in Range("1:10")
    assert 5 in Range("1:10")


def test_doesnt_contain_int():
    assert 0 not in Range("1:10")
    assert 10 not in Range("1:10")


def test_contains_sequence():
    assert (1, 2, 3, 4, 5) in Range("1:6")


def test_doesnt_contain_sequence():
    assert (1, 2, 3, 4, 5) not in Range("1:5")


def test_contains_range():
    assert Range("1:5") in Range("1:10")
    assert Range("2:10") in Range("2:")


def test_doesnt_contain_range():
    assert Range(":") not in Range("2:10")
    assert Range("1:10") not in Range("1:5")
    assert Range("2:") not in Range("2:10")


def test_nonetype_causes_error():
    with pytest.raises(TypeError):
        None in Range(":")


def test_nothing_in_empty():
    assert 1 not in Range("")
    assert [] not in Range(start=0, stop=0)
    assert Range("") not in Range("")


def test_contains_text_error():
    with pytest.raises(ValueError):
        "hello" in Range(":")


def test_contains_unsupported_type_error():
    class Crash:
        pass

    with pytest.raises(TypeError):
        Crash() in Range(":")
