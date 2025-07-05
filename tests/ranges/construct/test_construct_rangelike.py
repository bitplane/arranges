from arranges import Ranges


def test_construct_from_range():
    py = range(20, 30)
    ours = Ranges(py)

    assert ours == py
    assert ours == "20:30"


def test_construct_from_slice_step_1():
    py = slice(20, 30, 1)
    ours = Ranges(py)

    assert ours == py
    assert ours == "20:30"


def test_construct_from_range_with_step():
    actual = Ranges(range(10, 20, 2))
    expected = "10,12,14,16,18"
    assert actual == expected


def def_construct_boundless_slice():
    py = slice(20, None)
    ours = Ranges(py)

    assert ours == py
    assert ours == "20:"
