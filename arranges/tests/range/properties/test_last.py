from arranges import Range
from arranges.utils import inf


def test_last_inf():
    assert Range(":").last == inf


def test_last_num():
    assert Range(":10").last == 9
    assert Range("10").last == 10


def test_last_empty():
    assert Range("").last == -1
