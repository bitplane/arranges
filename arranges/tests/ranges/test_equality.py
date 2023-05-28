from arranges import Range, Ranges


def test_iterator():
    assert list(Ranges("1:5, 10:15")) == [1, 2, 3, 4, 10, 11, 12, 13, 14]


def test_range_ranges_equal():
    assert Ranges("10") == Range("0:10")
    assert Range("0:10") == Ranges("10")
