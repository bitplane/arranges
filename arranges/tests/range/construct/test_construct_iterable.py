import pytest

from arranges.ranges import Ranges


def test_construct_from_list():
    expected = [1, 2, 3, 4, 5]
    actual = Ranges(expected)

    assert actual == expected
    assert actual == "1:6"


def test_construct_from_tuple():
    expected = (1, 2, 3, 4, 5)
    actual = Ranges(expected)

    assert actual == expected
    assert actual == "1:6"


def test_construct_from_generator():
    def gen():
        for i in range(5):
            yield i

    expected = list(gen())
    actual = Ranges(gen())

    assert actual == expected


def test_construct_with_hole():
    expected = "1:3,4:6"
    actual = Ranges([1, 2, 4, 5])
    assert actual == expected


def test_duplicates():
    expected = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
    actual = Ranges(expected)

    assert actual == expected
    assert actual == "1:5"


def test_negatives_not_allowed():
    with pytest.raises(ValueError):
        Ranges([1, 2, 3, -1, 4, 5])


def test_from_sequence():
    ranges = Ranges([1, 2, 3, 4])

    assert ranges == Ranges("1:5")


def test_from_nested_mess():
    ranges = Ranges([[1, [2], ["101:201,30:31"], 3], range(10, 15)])

    assert ranges == Ranges("1:4,10:15,30:31,101:201")
