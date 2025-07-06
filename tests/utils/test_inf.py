import math
import sys

from arranges import inf


def test_is_infinity():
    assert inf == math.inf
    assert math.inf == inf


def test_is_max_size():
    assert inf == sys.maxsize
    assert sys.maxsize == inf


def test_is_bigger_than_max_size():
    assert inf > sys.maxsize
    assert sys.maxsize < inf


def test_to_int_with_start():
    """Test to_int with special 'start' value"""
    from arranges.utils import to_int

    # "start" should return 0
    assert to_int("start", 999) == 0
