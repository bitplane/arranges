from arranges import Arranged, Range


def test_collapse_ranges():
    assert Arranged("0:10, 20:") == Arranged(":0x0a, 0x14:")
    assert Arranged(":,:") == Arranged(":")
    assert Arranged("1:10, 5:15") == Arranged("1:15")


def test_combine_two_ranges():
    first = Arranged("1:10, 20:30")
    second = Arranged("0:5, 100:200")
    combined = first + second
    expected = Arranged("0:10,20:30,100:200")

    assert first in combined
    assert second in combined
    assert expected == combined


def test_combine_ranges_with_single_range():
    first = Arranged("1:10, 20:30")
    second = Range("0:5")
    combined = first + second
    expected = Arranged("0:10,20:30")

    assert first in combined
    assert second in combined
    assert combined == expected


def test_combine_ranges_with_string():
    first = Arranged("1:10, 20:30")
    second = "0:5"
    combined = first + second
    expected = Arranged("0:10,20:30")

    assert first in combined
    assert second in combined
    assert combined == expected


def test_combine_ranges_with_overlap():
    first = Arranged("11:15,20:25")
    second = Arranged("0:12, 100:")
    combined = first + second
    expected = Arranged("0:15,20:25,100:")

    assert first in combined
    assert second in combined
    assert combined == expected


def test_intersects():
    first = Arranged("11:15,20:25")
    second = Arranged("0:12, 100:")

    assert first.intersects(second)
    assert second.intersects(first)


def test_doesnt_overlap():
    first = Arranged("15")
    second = Arranged("15:")

    assert not first.intersects(second)
    assert not second.intersects(first)
