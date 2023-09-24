import pytest

from arranges import Ranges


def test_start_and_stop():
    r = Ranges(10, 20)

    assert r.first == 10
    assert r.last == 19


def test_length_1():
    assert Ranges(1) == "0"


def test_value_with_integer():
    r = Ranges(2)

    assert r.first == 0
    assert r.last == 1


def test_range_from_range():
    first = Ranges(1)
    second = Ranges(first)

    assert first == second


def test_error_on_empty_args():
    with pytest.raises(TypeError):
        Ranges()


def test_empty_range():
    empty1 = Ranges(0, 0)
    empty2 = Ranges(100, 100)

    assert empty1 == empty2
    assert empty1 == empty2 == ""


def test_range_with_negative_start():
    with pytest.raises(ValueError):
        Ranges(-1, 2)


def test_range_with_negative_stop():
    with pytest.raises(ValueError):
        Ranges(1, -2)


def test_same_behaviour_as_range():
    assert range(10) == Ranges(10)
    assert Ranges(1, 2) == range(1, 2)


def test_same_behaviour_as_slice():
    assert slice(10) == Ranges(10)
    assert Ranges(1, 2) == slice(1, 2)
