from arange import Range, inf


def test_equality():
    assert Range(":") == Range("0:")
    assert Range(":10") == Range("0:10")


def test_equality_str():
    assert Range("") == ""
    assert Range(":") != ""
    assert Range(":10") == "0:10"


def test_equality_int():
    assert Range("0:1") == 0
    assert Range("10:11") == 10
    assert Range("11") != 10


def test_equality_range_slice():
    assert Range("0:1") == range(0, 1)
    assert Range(":11") == slice(None, 11)
    assert Range(100, inf) == slice(100, None)
    assert Range("") == range(0, 0)
    assert Range(0, inf) == slice(None, None)
