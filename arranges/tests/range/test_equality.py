from arranges import Range, inf


def test_equality():
    assert Range(":") == Range("0:")
    assert Range(":10") == Range("0:10")


def test_equality_str_right():
    assert Range("") == ""
    assert Range(":") != ""
    assert Range(":10") == "0000:00010"


def test_equality_str_left():
    assert "" == Range(0, 0)
    assert "0:10" == Range(0, 10)
    assert ":10" == Range(0, 10)


def test_equality_int_right():
    assert Range("0:1") == [0]
    assert Range("10:11") == [10]
    assert Range("11") == [11]


def test_equality_int_left():
    assert [0] == Range("0:1")
    assert [10] == Range("10:11")
    assert [11] == Range("11")


def test_equality_range_right():
    assert Range("0:1") == range(0, 1)
    assert Range("") == range(0, 0)
    assert Range(":10") == range(0, 10)


def test_equality_range_left():
    assert range(0, 1) == Range("0:1")
    assert range(0, 0) == Range("")
    assert range(0, 10) == Range(":10")


def test_equality_slice_right():
    assert Range(100, inf) == slice(100, None)
    assert Range(0, 10) == slice(0, 10)


def test_equality_slice_left():
    assert slice(100, None) == Range(100, inf)
    assert slice(0, 10) == Range(0, 10)


def test_equality_with_step():
    assert range(10, 20, 2) != Range("10:20")
    assert Range("10:20") != range(10, 20, 2)
    assert range(10, 20, 1) == Range("10:20")
    assert Range("10:20") == range(10, 20, 1)


def test_not_equal_to_unknown_type():
    class Unknown:
        pass

    assert Range(":") != Unknown()
