import pytest

from arranges.range import Range
from arranges.utils import inf


def test_too_many_values():
    with pytest.raises(ValueError):
        Range("1:2:3")


def test_range_negative_start():
    with pytest.raises(ValueError):
        Range("-1:2")


def test_range_negative_stop():
    with pytest.raises(ValueError):
        Range("1:-2")


def test_range_no_first():
    val = Range(":2")

    assert val.first == 0
    assert val.last == 1


def test_range_no_last():
    val = Range("1:")

    assert val.first == 1
    assert val.last == inf


def test_range_no_start_no_last():
    val = Range(":")

    assert val.first == 0
    assert val.last == inf


def test_hex_range():
    assert Range("0x1:0x10") == Range("1:16")


def test_binary_range():
    assert Range("0b0:0b100") == Range(":4")


def test_octal_range():
    assert Range("0o0:0o10") == Range(":8")


def test_invalid_ints():
    with pytest.raises(ValueError):
        Range("bleep:bloop")


def test_full_range():
    assert Range("0:inf") == Range(":")


def test_start_after_stop():
    with pytest.raises(ValueError):
        Range("10:1")


def test_empty_str():
    empty_str_range = Range("")
    empty_range = Range(0, 0)

    assert empty_range == empty_str_range
    assert len(empty_range) == len(empty_str_range) == 0
