from arranges import Ranges


def test_inverted_empty_is_full():
    actual = ~Ranges("")
    expected = Ranges(":")
    assert actual == expected


def test_inverted_full_is_empty():
    actual = ~Ranges(":")
    expected = Ranges("")
    assert actual == expected


def test_inverted_range():
    actual = ~Ranges("5:10")
    expected = Ranges(":5,10:")
    assert actual == expected


def test_inverted_complex_range():
    actual = ~Ranges("2,4,6,8:50")
    expected = Ranges(":2,3,5,7,50:")
    assert actual == expected
