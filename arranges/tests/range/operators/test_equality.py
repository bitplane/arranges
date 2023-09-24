from arranges import Ranges, inf


def test_equality():
    assert Ranges(":") == Ranges("0:")
    assert Ranges(":10") == Ranges("0:10")


def test_equality_str_right():
    assert Ranges("") == ""
    assert Ranges(":") != ""
    assert Ranges(":10") == "0000:00010"


def test_equality_str_left():
    assert "" == Ranges(0, 0)
    assert "0:10" == Ranges(0, 10)
    assert ":10" == Ranges(0, 10)


def test_equality_int_right():
    assert Ranges("0:1") == [0]
    assert Ranges("10:11") == [10]
    assert Ranges("11") == [11]


def test_equality_int_left():
    assert [0] == Ranges("0:1")
    assert [10] == Ranges("10:11")
    assert [11] == Ranges("11")


def test_equality_range_right():
    assert Ranges("0:1") == range(0, 1)
    assert Ranges("") == range(0, 0)
    assert Ranges(":10") == range(0, 10)


def test_equality_range_left():
    assert range(0, 1) == Ranges("0:1")
    assert range(0, 0) == Ranges("")
    assert range(0, 10) == Ranges(":10")


def test_equality_slice_right():
    assert Ranges(100, inf) == slice(100, None)
    assert Ranges(0, 10) == slice(0, 10)


def test_equality_slice_left():
    assert slice(100, None) == Ranges(100, inf)
    assert slice(0, 10) == Ranges(0, 10)


def test_equality_with_step():
    assert range(10, 20, 2) != Ranges("10:20")
    assert Ranges("10:20") != range(10, 20, 2)
    assert range(10, 20, 1) == Ranges("10:20")
    assert Ranges("10:20") == range(10, 20, 1)


def test_not_equal_to_unknown_type():
    class Unknown:
        pass

    assert Ranges(":") != Unknown()
