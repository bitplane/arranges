from arranges.range import Range


def test_collapse_ranges():
    assert Range("0:10, 20:") == Range(":0x0a, 0x14:")
    assert Range(":,:") == Range(":")
    assert Range("1:10, 5:15") == Range("1:15")


def test_combine_two_ranges():
    first = Range("1:10, 20:30")
    second = Range("0:5, 100:200")
    combined = first + second
    expected = Range("0:10,20:30,100:200")

    assert first in combined
    assert second in combined
    assert expected == combined


def test_combine_ranges_with_single_range():
    first = Range("1:10, 20:30")
    second = Range("0:5")
    combined = first + second
    expected = Range("0:10,20:30")

    assert first in combined
    assert second in combined
    assert combined == expected


def test_combine_ranges_with_string():
    first = Range("1:10, 20:30")
    second = "0:5"
    combined = first + second
    expected = Range("0:10,20:30")

    assert first in combined
    assert second in combined
    assert combined == expected


def test_combine_ranges_with_overlap():
    first = Range("11:15,20:25")
    second = Range("0:12, 100:")
    combined = first + second
    expected = Range("0:15,20:25,100:")

    assert first in combined
    assert second in combined
    assert combined == expected


def test_intersects():
    first = Range("11:15,20:25")
    second = Range("0:12, 100:")

    assert first.intersects(second)
    assert second.intersects(first)


def test_doesnt_overlap():
    first = Range("14")
    second = Range("15:")

    assert not first.intersects(second)
    assert not second.intersects(first)
