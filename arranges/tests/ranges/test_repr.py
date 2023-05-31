from arranges import Arranged


def test_repr():
    ranges = Arranged(" 0x01:0b10, 15:20 , 30:")
    assert repr(ranges) == type(ranges).__name__ + '("1:2,15:20,30:")'


def test_str():
    ranges = Arranged(" 0x01:0b10, 15:20 , 30:    ")
    assert str(ranges) == "1:2,15:20,30:"
