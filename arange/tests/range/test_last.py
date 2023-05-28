from arange import Range
from arange.utils import inf


def test_last_inf():
    assert Range(":").last == inf


def test_last_num():
    assert Range("10").last == 9


def test_last_empty():
    assert Range("").last == -1
