from arranges.utils import try_hash


def test_hashable():
    assert try_hash("hey") == hash("hey")


def test_unhashable():
    assert not try_hash({})


def test_as_type_with_same_type():
    """Test as_type when value is already correct type"""
    from arranges.utils import as_type

    # When value is already the correct type, should return it directly
    s = "hello"
    result = as_type(str, s)
    assert result is s  # Should be the same object, not a copy
