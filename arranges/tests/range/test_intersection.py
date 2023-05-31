from arranges.range import Range


def r(s: str) -> Range:
    """
    Make a Range from a string.
    """
    return Range([i for i, c in enumerate(s) if c != " "])


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
