from arange import Range
from arange.utils import inf


def test_last():
    assert Range("").last == inf
    assert Range("10").last == 9
