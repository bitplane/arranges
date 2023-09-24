from arranges import Range


def test_inverted_empty_is_full():
    actual = ~Range("")
    expected = Range(":")
    assert actual == expected


def test_inverted_full_is_empty():
    actual = ~Range(":")
    expected = Range("")
    assert actual == expected


def test_inverted_range():
    actual = ~Range("5:10")
    expected = Range(":5,10:")
    assert actual == expected


def test_inverted_complex_range():
    actual = ~Range("2,4,6,8:50")
    expected = Range(":2,3,5,7,50:")
    assert actual == expected
