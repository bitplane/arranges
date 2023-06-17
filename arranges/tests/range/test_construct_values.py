import pytest

from arranges import Range


def test_start_and_stop():
    r = Range(10, 20)

    assert r.start == 10
    assert r.stop == 20


def test_value_with_integer():
    r = Range(2)

    assert r.start == 0
    assert r.stop == 2


def test_range_from_range():
    first = Range(1)
    second = Range(first)

    assert first == second


def test_error_on_empty_args():
    with pytest.raises(TypeError):
        Range()


def test_empty_range():
    empty1 = Range(0, 0)
    empty2 = Range(100, 100)

    assert empty1 == empty2
    assert empty1.start == empty1.stop == empty2.start == empty2.stop == 0
    assert empty1 == empty2 == ""


def test_range_with_negative_start():
    with pytest.raises(ValueError):
        Range(-1, 2)


def test_range_with_negative_stop():
    with pytest.raises(ValueError):
        Range(1, -2)


def test_same_behaviour_as_range():
    assert range(10) == Range(10)
    assert Range(1, 2) == range(1, 2)


def test_same_behaviour_as_slice():
    assert slice(10) == Range(10)
    assert Range(1, 2) == slice(1, 2)
