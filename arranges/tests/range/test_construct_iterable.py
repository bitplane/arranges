import pytest

from arranges.range import Range


def test_construct_from_list():
    expected = [1, 2, 3, 4, 5]
    actual = Range(expected)

    assert actual == expected
    assert actual == "1:6"


def test_construct_from_tuple():
    expected = (1, 2, 3, 4, 5)
    actual = Range(expected)

    assert actual == expected
    assert actual == "1:6"


def test_construct_from_generator():
    def gen():
        for i in range(5):
            yield i

    expected = list(gen())
    actual = Range(gen())

    assert actual == expected


def test_construct_with_hole():
    expected = "1:3,4:6"
    actual = Range([1, 2, 4, 5])
    assert actual == expected


def test_duplicates():
    expected = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
    actual = Range(expected)

    assert actual == expected
    assert actual == "1:5"


def test_negatives_not_allowed():
    with pytest.raises(ValueError):
        Range([1, 2, 3, -1, 4, 5])
