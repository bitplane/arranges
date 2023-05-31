from arranges import Range


def test_full_range():
    assert hash(Range(":")) == hash(Range("0:inf"))


def test_empty_range():
    assert hash(Range("")) == hash(Range(0, 0))


def test_hash_is_str_hash():
    assert hash(Range(":10")) == hash("10")
