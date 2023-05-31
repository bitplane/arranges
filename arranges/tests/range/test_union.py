from arranges import Range


def test_join():
    assert Range("1:10").union(Range("5:15")) == Range("1:15")
    assert Range(":10").union(Range("9:")) == Range(":")


def test_join_adjacent():
    assert Range("1:10").union(Range("10:15")) == Range("1:15")
    assert Range("1:10").union(Range("0:1")) == Range("0:10")


def test_intersects():
    assert Range("1:10").intersects(Range("5:15"))
    assert Range(":10").intersects(Range("9:"))

    assert Range("5:10").intersects(Range(":"))
    assert Range(":").intersects(Range(":"))
    assert Range("1:100").intersects(Range("0:1000"))

    assert not Range("1:10").intersects(Range("11:15"))
    assert not Range("1:10").intersects(Range("11:"))


def test_isadjacent():
    assert Range("1:10").isadjacent(Range("10:15"))
    assert Range("1:10").isadjacent(Range("0:1"))


def test_not_adjacent():
    assert not Range("1:10").isadjacent(Range("0:10"))
    assert not Range("1:10").isadjacent(Range("11:15"))
    assert not Range("1:10").isadjacent(Range("11:"))
