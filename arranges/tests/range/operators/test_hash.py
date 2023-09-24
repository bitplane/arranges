from arranges import Ranges


def test_full_range():
    assert hash(Ranges(":")) == hash(Ranges("0:inf"))


def test_empty_range():
    assert hash(Ranges("")) == hash(Ranges(0, 0))


def test_hash_is_str_hash():
    assert hash(Ranges(":10")) == hash(":10")
