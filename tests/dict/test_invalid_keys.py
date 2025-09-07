"""Test Dict behavior with invalid range keys"""

import pytest
from arranges import Dict


def test_contains_with_invalid_key():
    """Invalid keys should return False in containment checks"""
    d = Dict()
    d[100:200] = "highlight"

    # Invalid range keys should return False, not raise
    assert "invalid_key" not in d
    assert "not-a-range" not in d
    assert "abc123" not in d

    # Valid range keys work normally
    assert 150 in d
    assert "100:200" in d


def test_get_with_invalid_key():
    """Invalid keys should return default in get() calls"""
    d = Dict()
    d[100:200] = "highlight"

    # Invalid range keys should return None/default, not raise
    assert d.get("invalid_key") is None
    assert d.get("not-a-range") is None
    assert d.get("abc123", "default") == "default"

    # Valid range keys work normally
    assert d.get("100:200") == "highlight"
    assert d.get("300:400") is None  # Valid range, just not stored


def test_getitem_with_invalid_key_raises():
    """Invalid keys should still raise in __getitem__ (strict access)"""
    d = Dict()
    d[100:200] = "highlight"

    # Invalid range keys should raise in direct access
    with pytest.raises(ValueError):
        d["invalid_key"]

    with pytest.raises(ValueError):
        d["not-a-range"]


def test_setitem_with_invalid_key_raises():
    """Invalid keys should raise in __setitem__ (strict mutation)"""
    d = Dict()

    # Invalid range keys should raise in assignment
    with pytest.raises(ValueError):
        d["invalid_key"] = "value"

    with pytest.raises(ValueError):
        d["not-a-range"] = "value"


def test_delitem_with_invalid_key_raises():
    """Invalid keys should raise in __delitem__ (strict mutation)"""
    d = Dict()
    d[100:200] = "highlight"

    # Invalid range keys should raise in deletion
    with pytest.raises(ValueError):
        del d["invalid_key"]


def test_pop_with_invalid_key_raises():
    """Invalid keys should raise in pop() (strict access)"""
    d = Dict()
    d[100:200] = "highlight"

    # Invalid range keys should raise in pop
    with pytest.raises(ValueError):
        d.pop("invalid_key")

    # Even with default
    with pytest.raises(ValueError):
        d.pop("invalid_key", "default")


def test_setdefault_with_invalid_key_raises():
    """Invalid keys should raise in setdefault() (mutation)"""
    d = Dict()

    # Invalid range keys should raise in setdefault
    with pytest.raises(ValueError):
        d.setdefault("invalid_key", "value")


def test_update_with_invalid_keys_raises():
    """Invalid keys should raise in update() (mutation)"""
    d = Dict()

    # Invalid range keys should raise in update
    with pytest.raises(ValueError):
        d.update({"invalid_key": "value"})

    with pytest.raises(ValueError):
        d.update([("not-a-range", "value")])


def test_mixed_valid_invalid_keys():
    """Mix of valid and invalid keys should work predictably"""
    d = Dict()
    d[100:200] = "highlight"
    d[300:400] = "selection"

    # Valid keys work
    assert 150 in d
    assert d.get("100:200") == "highlight"

    # Invalid keys return False/None
    assert "invalid" not in d
    assert d.get("invalid") is None

    # But still raise in mutations
    with pytest.raises(ValueError):
        d["invalid"] = "value"
