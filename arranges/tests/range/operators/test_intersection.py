from arranges import Ranges


def r(s: str) -> Ranges:
    """
    Make a Range from a string.
    """
    return Ranges([i for i, c in enumerate(s) if c != " "])


def test_left_overlap():
    a = "             *********** "
    b = "         ******** "
    c = "             **** "

    assert r(a) & r(b) == r(c)


def test_right_overlap():
    a = "             ***********      "
    b = "                     ******** "
    c = "                     ***      "
    assert r(a) & r(b) == r(c)


def test_larger():
    a = "             ***********      "
    b = "          *****************   "
    c = "             ***********      "
    assert r(a) & r(b) == r(c)


def test_smaller():
    a = "             ***********      "
    b = "               *******        "
    c = "               *******        "
    assert r(a) & r(b) == r(c)


def test_no_overlap_left():
    a = "             *********** "
    b = " ****** "
    c = ""
    assert r(a) & r(b) == r(c)


def test_no_overlap_right():
    a = "             *********** "
    b = "                           ***** "
    c = ""
    assert r(a) & r(b) == r(c)


def test_both_empty():
    a = ""
    b = ""
    c = ""
    assert r(a) & r(b) == r(c)


def test_second_empty():
    a = "      **** "
    b = ""
    c = ""
    assert r(a) & r(b) == r(c)


def test_first_empty():
    a = ""
    b = " *** "
    c = ""
    assert r(a) & r(b) == r(c)
