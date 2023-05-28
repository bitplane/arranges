from arranges import Ranges


def test_repr():
    ranges = Ranges(" 0x01:0b10, 15:20 , 30:")
    assert repr(ranges) == 'Ranges("1:2,15:20,30:")'


def test_str():
    ranges = Ranges(" 0x01:0b10, 15:20 , 30:    ")
    assert str(ranges) == "1:2,15:20,30:"
