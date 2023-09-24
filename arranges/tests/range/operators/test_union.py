from arranges import Ranges


def test_join():
    assert Ranges("1:10").union(Ranges("5:15")) == Ranges("1:15")
    assert Ranges(":10").union(Ranges("9:")) == Ranges(":")


def test_join_adjacent():
    assert Ranges("1:10").union(Ranges("10:15")) == Ranges("1:15")
    assert Ranges("1:10").union(Ranges("0:1")) == Ranges("0:10")


def test_intersects():
    assert Ranges("1:10").intersects(Ranges("5:15"))
    assert Ranges(":10").intersects(Ranges("9:"))

    assert Ranges("5:10").intersects(Ranges(":"))
    assert Ranges(":").intersects(Ranges(":"))
    assert Ranges("1:100").intersects(Ranges("0:1000"))

    assert not Ranges("1:10").intersects(Ranges("11:15"))
    assert not Ranges("1:10").intersects(Ranges("11:"))
