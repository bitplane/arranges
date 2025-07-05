from arranges import Ranges


def test_or_operator():
    """
    Like with a set, or means union
    """
    assert Ranges("1:10") | Ranges("5:15") == Ranges("1:15")
    assert Ranges(":10") | Ranges("9:") == Ranges(":")


def test_or_operator_empty_range():
    expected = Ranges("1:10")
    empty = Ranges("0:0")

    actual_left = expected | empty
    actual_right = empty | expected

    assert actual_left == expected
    assert actual_right == expected


def test_or_operator_non_overlapping():
    combined = Ranges("1:10") | Ranges("11:15")
    assert combined == "1:10,11:15"


def test_union_adjacent_ranges():
    union = Ranges("0:5") | Ranges("5:10")
    assert union == "0:10"


def test_iterator():
    assert list(Ranges("1:10")) == [1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert list(Ranges(":5")) == [0, 1, 2, 3, 4]
    assert list(Ranges("3")) == [3]
