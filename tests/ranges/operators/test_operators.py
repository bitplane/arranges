from arranges import Ranges


def test_or_operator():
    """
    Like with a set, or means union
    """
    assert Ranges("1:10") | Ranges("5:15") == Ranges("1:15")
    assert Ranges(":10") | Ranges("9:") == Ranges(":")


def test_or_operator_empty_range():
    expected = Ranges("1:10")
    empty = Ranges("0:0")

    actual_left = expected | empty
    actual_right = empty | expected

    assert actual_left == expected
    assert actual_right == expected


def test_or_operator_non_overlapping():
    combined = Ranges("1:10") | Ranges("11:15")
    assert combined == "1:10,11:15"


def test_union_adjacent_ranges():
    union = Ranges("0:5") | Ranges("5:10")
    assert union == "0:10"


def test_iterator():
    assert list(Ranges("1:10")) == [1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert list(Ranges(":5")) == [0, 1, 2, 3, 4]
    assert list(Ranges("3")) == [3]


def test_subset_operator():
    """
    Test subset operator (<=)
    """
    assert Ranges("1:5") <= Ranges("1:10")
    assert Ranges("1:5") <= Ranges("1:5")
    assert Ranges("") <= Ranges("1:5")
    assert not (Ranges("1:10") <= Ranges("1:5"))
    assert not (Ranges("1:5") <= Ranges("2:6"))


def test_proper_subset_operator():
    """
    Test proper subset operator (<)
    """
    assert Ranges("1:5") < Ranges("1:10")
    assert Ranges("") < Ranges("1:5")
    assert not (Ranges("1:5") < Ranges("1:5"))
    assert not (Ranges("1:10") < Ranges("1:5"))
    assert not (Ranges("1:5") < Ranges("2:6"))


def test_superset_operator():
    """
    Test superset operator (>=)
    """
    assert Ranges("1:10") >= Ranges("1:5")
    assert Ranges("1:5") >= Ranges("1:5")
    assert Ranges("1:5") >= Ranges("")
    assert not (Ranges("1:5") >= Ranges("1:10"))
    assert not (Ranges("1:5") >= Ranges("2:6"))


def test_proper_superset_operator():
    """
    Test proper superset operator (>)
    """
    assert Ranges("1:10") > Ranges("1:5")
    assert Ranges("1:5") > Ranges("")
    assert not (Ranges("1:5") > Ranges("1:5"))
    assert not (Ranges("1:5") > Ranges("1:10"))
    assert not (Ranges("1:5") > Ranges("2:6"))


def test_relative_complement_operator():
    """
    Test relative complement operator (-)
    """
    assert Ranges("1:10") - Ranges("3:7") == Ranges("1:3,7:10")
    assert Ranges("1:10") - Ranges("1:5") == Ranges("5:10")
    assert Ranges("1:10") - Ranges("5:10") == Ranges("1:5")
    assert Ranges("1:10") - Ranges("1:10") == Ranges("")
    assert Ranges("1:10") - Ranges("") == Ranges("1:10")
    assert Ranges("") - Ranges("1:10") == Ranges("")


def test_symmetric_difference():
    """
    Test symmetric difference (A | B) - (A & B)
    """
    a = Ranges("1:5")
    b = Ranges("3:7")
    expected = Ranges("1:3,5:7")
    assert (a | b) - (a & b) == expected

    a = Ranges("1:5")
    b = Ranges("6:10")
    expected = Ranges("1:5,6:10")
    assert (a | b) - (a & b) == expected

    a = Ranges("1:5")
    b = Ranges("1:5")
    expected = Ranges("")
    assert (a | b) - (a & b) == expected


def test_cardinality():
    """
    Test cardinality (len)
    """
    assert len(Ranges("1:10")) == 9
    assert len(Ranges(":5")) == 5
    assert len(Ranges("3")) == 1
    assert len(Ranges("1:5,7:10")) == 7
    assert len(Ranges("")) == 0
