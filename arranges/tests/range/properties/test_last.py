from arranges import Ranges
from arranges.utils import inf


def test_last_inf():
    assert Ranges(":").last == inf


def test_last_num():
    assert Ranges(":10").last == 9
    assert Ranges("10").last == 10


def test_last_empty():
    assert Ranges("").last == -1
