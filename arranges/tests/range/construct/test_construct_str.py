import pytest

from arranges import Ranges, inf


def test_too_many_values():
    with pytest.raises(ValueError):
        Ranges("1:2:3")


def test_range_negative_start():
    with pytest.raises(ValueError):
        Ranges("-1:2")


def test_range_negative_stop():
    with pytest.raises(ValueError):
        Ranges("1:-2")


def test_range_no_first():
    val = Ranges(":2")

    assert val.first == 0
    assert val.last == 1


def test_range_no_last():
    val = Ranges("1:")

    assert val.first == 1
    assert val.last == inf


def test_range_no_start_no_last():
    val = Ranges(":")

    assert val.first == 0
    assert val.last == inf


def test_hex_range():
    assert Ranges("0x1:0x10") == Ranges("1:16")


def test_binary_range():
    assert Ranges("0b0:0b100") == Ranges(":4")


def test_octal_range():
    assert Ranges("0o0:0o10") == Ranges(":8")


def test_invalid_ints():
    with pytest.raises(ValueError):
        Ranges("bleep:bloop")


def test_full_range():
    assert Ranges("0:inf") == Ranges(":")


def test_start_after_stop():
    with pytest.raises(ValueError):
        Ranges("10:1")


def test_empty_str():
    empty_str_range = Ranges("")
    empty_range = Ranges(0, 0)

    assert empty_range == empty_str_range
    assert len(empty_range) == len(empty_str_range) == 0


def test_parse_single_range():
    r = Ranges("1:10")
    assert len(r.segments) == 1
    assert r.segments[0].start == 1
    assert r.segments[0].stop == 10


def test_parse_multiple_ranges():
    r = Ranges("1:10, 20:30")

    assert len(r.segments) == 2
    assert r.segments[0].start == 1
    assert r.segments[0].stop == 10
    assert r.segments[1].start == 20
    assert r.segments[1].stop == 30
