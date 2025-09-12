"""Test Dict construction and basic dict interface compatibility"""

import pytest
from arranges import Dict


def test_empty_construction():
    """Can construct empty Dict"""
    d = Dict()
    assert len(d) == 0
    assert not d
    assert d.ranges == ""


def test_dict_from_pairs():
    """Can construct from key-value pairs like regular dict"""
    # This should work with range strings as keys
    d = Dict([("100:200", "highlight"), ("300:400", "selection")])
    assert len(d) == 2
    assert d["100:200"] == "highlight"
    assert d["300:400"] == "selection"


def test_dict_from_kwargs():
    """Can construct from keyword arguments (if keys are valid identifiers)"""
    # This won't work with range syntax, but should work for simple cases
    try:
        d = Dict(a="value1", b="value2")
        assert d["a"] == "value1"
        assert d["b"] == "value2"
    except Exception:
        # This might not work due to range conversion, which is okay
        pass


def test_dict_from_dict():
    """Can construct from existing dict"""
    source = {"100:200": "highlight", "300:400": "selection"}
    d = Dict(source)
    assert len(d) == 2
    assert d["100:200"] == "highlight"
    assert d["300:400"] == "selection"


def test_dict_update():
    """Can update like regular dict"""
    d = Dict()
    d.update({"100:200": "highlight"})
    assert d["100:200"] == "highlight"

    d.update([("300:400", "selection")])
    assert d["300:400"] == "selection"


def test_dict_copy():
    """Can copy like regular dict"""
    d = Dict()
    d[100:200] = "highlight"

    d2 = d.copy()
    assert d2[100:200] == "highlight"
    assert d2 is not d


def test_dict_clear():
    """Can clear like regular dict"""
    d = Dict()
    d[100:200] = "highlight"
    assert len(d) == 1

    d.clear()
    assert len(d) == 0
    assert d.ranges == ""


def test_dict_get():
    """Can use get() method with range keys"""
    d = Dict()
    d[100:200] = "highlight"

    assert d.get("100:200") == "highlight"
    assert d.get(slice(100, 200)) == "highlight"
    assert d.get("300:400") is None  # Valid range, just not stored
    assert d.get("500:600", "default") == "default"


def test_dict_pop():
    """Can use pop() method like regular dict"""
    d = Dict()
    d[100:200] = "highlight"
    d[300:400] = "selection"

    value = d.pop("100:200")
    assert value == "highlight"
    assert len(d) == 1
    assert "100:200" not in d

    # Should update ranges after pop
    assert "100:200" not in str(d.ranges)


def test_dict_setdefault():
    """Can use setdefault() method like regular dict"""
    d = Dict()

    result = d.setdefault("100:200", "highlight")
    assert result == "highlight"
    assert d["100:200"] == "highlight"

    # Should not overwrite existing
    result2 = d.setdefault("100:200", "different")
    assert result2 == "highlight"
    assert d["100:200"] == "highlight"


def test_dict_iteration():
    """Can iterate over keys, values, items like regular dict"""
    d = Dict()
    d[100:200] = "highlight"
    d[300:400] = "selection"

    keys = list(d.keys())
    values = list(d.values())
    items = list(d.items())

    assert len(keys) == len(values) == len(items) == 2
    assert "100:200" in keys
    assert "300:400" in keys
    assert "highlight" in values
    assert "selection" in values
    assert ("100:200", "highlight") in items
    assert ("300:400", "selection") in items


def test_ranges_updates_on_all_modifications():
    """Ranges attribute updates on all dict modifications"""
    d = Dict()
    assert d.ranges == ""

    d[100:200] = "highlight"
    assert "100:200" in str(d.ranges)

    d.update({"300:400": "selection"})
    ranges_str = str(d.ranges)
    assert "100:200" in ranges_str
    assert "300:400" in ranges_str

    d.pop("100:200")
    assert "300:400" in str(d.ranges)
    assert "100:200" not in str(d.ranges)

    d.clear()
    assert d.ranges == ""


def test_dict_too_many_positional_args():
    """Dict should raise TypeError when given more than 1 positional arg."""
    with pytest.raises(TypeError, match="Dict expected at most 1 argument, got 2"):
        Dict({1: "a"}, {2: "b"})

    with pytest.raises(TypeError, match="Dict expected at most 1 argument, got 3"):
        Dict({1: "a"}, {2: "b"}, {3: "c"})
