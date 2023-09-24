import pytest

from arranges import Range


def test_parse_single_range():
    r = Range("1:10")
    assert len(r.segments) == 1
    assert r.segments[0].start == 1
    assert r.segments[0].stop == 10


def test_parse_multiple_ranges():
    r = Range("1:10, 20:30")

    assert len(r.segments) == 2
    assert r.segments[0].start == 1
    assert r.segments[0].stop == 10
    assert r.segments[1].start == 20
    assert r.segments[1].stop == 30


def test_from_sequence():
    ranges = Range([1, 2, 3, 4])

    assert ranges == Range("1:5")


def test_from_nested_mess():
    ranges = Range([[1, [2], ["101:201,30:31"], 3], range(10, 15)])

    assert ranges == Range("1:4,10:15,30:31,101:201")


def test_from_unsupported_type():
    with pytest.raises(TypeError):
        Range(None)
