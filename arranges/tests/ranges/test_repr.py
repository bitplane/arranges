import pytest

from arranges import Ranges


def test_repr():
    ranges = Ranges(" 0x01:0b10, 15:20 , 30:")
    assert repr(ranges) == type(ranges).__name__ + '("1,15:20,30:")'


def test_str():
    ranges = Ranges(" 0x01:0b10, 15:20 , 30:    ")
    assert str(ranges) == "1,15:20,30:"


def test_hash():
    """
    This is a mutable type so it can't be hashed.
    """
    with pytest.raises(TypeError):
        hash(Ranges("1:10, 20:30"))
