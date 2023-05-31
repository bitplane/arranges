from arranges import Arranged, Range


def test_membership_int():
    ranges = Arranged("1:10,20:30,100:150")

    assert 0 not in ranges
    assert 1 in ranges
    assert 5 in ranges
    assert 10 not in ranges
    assert 19 not in ranges
    assert 20 in ranges
    assert 30 not in ranges
    assert 100 in ranges
    assert 149 in ranges
    assert 150 not in ranges


def test_membership_sequence():
    ranges = Arranged("1:10,20:30,100:150")

    assert range(10, 15) not in ranges
    assert range(100, 110) in ranges


def test_membership_range():
    ranges = Arranged("1:10,20:30,100:150")

    assert Range(20, 30) in ranges


def test_membership_empty_range():
    ranges = Arranged("1:10,20:30,100:150")
    empty = Range(0, 0)

    assert empty in ranges
