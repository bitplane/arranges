import pytest

from arange import Ranges


def test_parse_single_range():
    r = Ranges("1:10")
    assert len(r.ranges) == 1
    assert r.ranges[0].start == 1
    assert r.ranges[0].stop == 10


def test_parse_multiple_ranges():
    r = Ranges("1:10, 20:30")

    assert len(r.ranges) == 2
    assert r.ranges[0].start == 1
    assert r.ranges[0].stop == 10
    assert r.ranges[1].start == 20
    assert r.ranges[1].stop == 30


def test_from_sequence():
    ranges = Ranges([1, 2, 3, 4])

    assert ranges == Ranges("1:5")


def test_from_nested_mess():
    ranges = Ranges([[1, [2], ["101:201,30:31"], 3], range(10, 15)])

    assert ranges == Ranges("1:4,10:15,30:31,101:201")


def test_from_unsupported_type():
    with pytest.raises(TypeError):
        Ranges(None)
