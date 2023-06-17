import pytest

from arranges import Range, inf


def test_construct_from_range():
    py = range(20, 30)
    ours = Range(py)

    assert ours == py
    assert ours.start == py.start
    assert ours.stop == py.stop
    assert ours.step == py.step == 1


def test_construct_from_slice():
    py = slice(20, 30, 1)
    ours = Range(py)

    assert ours == py
    assert ours.start == py.start
    assert ours.stop == py.stop
    assert ours.step == py.step == 1


def test_construct_from_slice_no_step():
    py = slice(20, 30)
    ours = Range(py)

    assert ours == py
    assert ours.start == py.start
    assert ours.stop == py.stop
    assert ours.step == 1


def test_construct_from_range_with_step():
    with pytest.raises(ValueError):
        Range(range(20, 30, 2))


def test_construct_from_slice_with_step():
    with pytest.raises(ValueError):
        Range(slice(20, 30, 2))


def def_construct_boundless_slice():
    py = slice(20, None)
    ours = Range(py)

    assert ours == py
    assert ours.start == py.start
    assert ours.stop == inf
