from arranges.segment import Segment


def test_isadjacent():
    assert Segment("1:10").isadjacent(Segment("10:15"))
    assert Segment("1:10").isadjacent(Segment("0:1"))


def test_not_adjacent():
    assert not Segment("1:10").isadjacent(Segment("0:10"))
    assert not Segment("1:10").isadjacent(Segment("11:15"))
    assert not Segment("1:10").isadjacent(Segment("11:"))
