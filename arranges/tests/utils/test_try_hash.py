from arranges.utils import try_hash


def test_hashable():
    assert try_hash("hey") == hash("hey")


def test_unhashable():
    assert not try_hash({})
