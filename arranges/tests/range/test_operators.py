from arranges import Range


def test_or_operator():
    """
    Like with a set, or means union
    """
    assert Range("1:10") | Range("5:15") == Range("1:15")
    assert Range(":10") | Range("9:") == Range(":")


def test_or_operator_empty_range():
    expected = Range("1:10")
    empty = Range("0:0")

    actual_left = expected | empty
    actual_right = empty | expected

    assert actual_left == expected
    assert actual_right == expected


def test_or_operator_non_overlapping():
    combined = Range("1:10") | Range("11:15")
    assert combined == "1:10,11:15"


def test_union_adjacent_ranges():
    union = Range("0:5") | Range("5:10")
    assert union == "0:10"


def test_iterator():
    assert list(Range("1:10")) == [1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert list(Range(":5")) == [0, 1, 2, 3, 4]
    assert list(Range("3")) == [3]
