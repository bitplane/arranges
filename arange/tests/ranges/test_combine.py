from arange import Range, Ranges


def test_collapse_ranges():
    assert Ranges("0:10, 20:") == Ranges(":0x0a, 0x14:")
    assert Ranges(":,:") == Ranges(":")
    assert Ranges("1:10, 5:15") == Ranges("1:15")


def test_combine_two_ranges():
    first = Ranges("1:10, 20:30")
    second = Ranges("0:5, 100:200")
    combined = first + second
    expected = Ranges("0:10,20:30,100:200")

    assert first in combined
    assert second in combined
    assert expected == combined


def test_combine_ranges_with_single_range():
    first = Ranges("1:10, 20:30")
    second = Range("0:5")
    combined = first + second
    expected = Ranges("0:10,20:30")

    assert first in combined
    assert second in combined
    assert combined == expected


def test_combine_ranges_with_string():
    first = Ranges("1:10, 20:30")
    second = "0:5"
    combined = first + second
    expected = Ranges("0:10,20:30")

    assert first in combined
    assert second in combined
    assert combined == expected


def test_combine_ranges_with_overlap():
    first = Ranges("11:15,20:25")
    second = Ranges("0:12, 100:")
    combined = first + second
    expected = Ranges("0:15,20:25,100:")

    assert first in combined
    assert second in combined
    assert combined == expected


def test_overlaps():
    first = Ranges("11:15,20:25")
    second = Ranges("0:12, 100:")

    assert first.overlaps(second)
    assert second.overlaps(first)


def test_doesnt_overlap():
    first = Ranges("15")
    second = Ranges("15:")

    assert not first.overlaps(second)
    assert not second.overlaps(first)
