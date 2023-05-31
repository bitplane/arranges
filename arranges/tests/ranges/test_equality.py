from arranges import Arranged, Range


def test_iterator():
    assert list(Arranged("1:5, 10:15")) == [1, 2, 3, 4, 10, 11, 12, 13, 14]


def test_range_ranges_equal():
    assert Arranged("10") == Range("0:10")
    assert Range("0:10") == Arranged("10")
