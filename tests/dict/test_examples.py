"""Design tests for Dict class - examples of intended usage"""

import pytest
from arranges import Dict, Ranges


def test_constructor_error_handling():
    """Dict constructor should handle argument errors like normal dict"""
    # Too many arguments should raise TypeError
    with pytest.raises(TypeError, match="Dict expected at most 1 argument, got 2"):
        Dict({"100:200": "value"}, {range(300, 400): "other"})

    # Single argument should work
    d = Dict({slice(100, 200): "value"})
    assert d[100:200] == "value"


def test_basic_range_to_value_mapping():
    """Basic case: map ranges to values using slice syntax"""
    highlights = Dict()
    highlights[100:200] = "search-match"
    highlights[300:400] = "selection"

    assert highlights[100:200] == "search-match"
    assert highlights[300:400] == "selection"

    # Individual positions within ranges
    assert 150 in highlights
    assert 350 in highlights
    assert 250 not in highlights


def test_slice_syntax_variants():
    """All Python slice syntaxes should work"""
    highlights = Dict()
    highlights[:100] = "start-highlight"  # From beginning
    highlights[200:] = "end-highlight"  # To end
    highlights[100:200] = "middle-highlight"  # Between
    highlights[:] = "full-highlight"  # Everything (overwrites all)

    assert highlights[50] == "full-highlight"
    assert highlights[150] == "full-highlight"
    assert highlights[250] == "full-highlight"


def test_overlapping_ranges_replace_policy():
    """When ranges overlap, later assignment replaces earlier"""
    highlights = Dict()
    highlights[100:200] = "search-match"
    highlights[150:250] = "selection"  # Overlaps with search-match

    # The overlapping part should now be "selection"
    assert highlights[100:150] == "search-match"  # Before overlap
    assert highlights[150:200] == "selection"  # Overlap area
    assert highlights[200:250] == "selection"  # After original


def test_adjacent_ranges_same_value_merge():
    """Adjacent ranges with same value should merge"""
    highlights = Dict()
    highlights[100:200] = "highlight"
    highlights[200:300] = "highlight"  # Same value, adjacent

    # Should merge into single range
    assert highlights[100:300] == "highlight"
    assert len(highlights) == 1  # Only one segment


def test_single_position_keys():
    """Integer keys represent single positions"""
    cursor = Dict()
    cursor[100] = "cursor"
    cursor[200] = "cursor"

    assert cursor[100] == "cursor"
    assert cursor[200] == "cursor"
    assert 99 not in cursor
    assert 101 not in cursor


def test_hex_editor_style_usage():
    """Hex editor style - complex values as metadata"""
    doc_meta = Dict()
    doc_meta[0x100:0x200] = {"type": "header", "color": "blue"}
    doc_meta[0x200:0x300] = {"type": "data", "color": "white"}
    doc_meta[0x150:0x180] = {"type": "modified", "color": "red"}  # Overlaps header

    # Modified section should replace part of header
    assert doc_meta[0x100:0x150]["type"] == "header"
    assert doc_meta[0x150:0x180]["type"] == "modified"
    assert doc_meta[0x180:0x200]["type"] == "header"


def test_none_assignment_example():
    """Assigning None stores None as a valid value"""
    highlights = Dict()
    highlights[100:300] = "highlight"
    highlights[150:200] = None  # Assign None as value

    assert highlights[100:150] == "highlight"
    assert highlights[150:200] is None  # None value
    assert highlights[200:300] == "highlight"
    assert 175 in highlights and highlights[175] is None  # Has None value


def test_multi_segment_ranges():
    """Use Ranges objects for complex multi-segment ranges"""
    highlights = Dict()
    multi_range = Ranges("100:200,300:400,500:600")
    highlights[multi_range] = "multi-selection"

    assert highlights[150] == "multi-selection"
    assert highlights[350] == "multi-selection"
    assert highlights[550] == "multi-selection"
    assert 250 not in highlights  # Gap between ranges


def test_terminal_scrollback_style():
    """Terminal emulator style usage with line ranges"""
    search_results = Dict()

    # Search for "error" found at multiple locations
    search_results[100:101] = {"term": "error", "match_id": 1}
    search_results[200:201] = {"term": "error", "match_id": 2}
    search_results[150:151] = {"term": "warning", "match_id": 3}

    # Current selection overlaps one search result
    selection = Dict()
    selection[99:102] = {"type": "selection"}

    assert search_results[100:101]["term"] == "error"
    assert selection[99:102]["type"] == "selection"


def test_efficient_large_ranges():
    """Should handle large ranges efficiently"""
    large_doc = Dict()

    # Map huge range to metadata without storing every position
    large_doc[:1000000] = {"type": "file_content", "source": "disk"}
    large_doc[500000:600000] = {"type": "modified", "in_memory": True}

    assert large_doc[250000]["type"] == "file_content"
    assert large_doc[550000]["type"] == "modified"

    # Should not store 1 million individual entries
    assert len(large_doc) <= 10  # Just a few segments


def test_string_range_fallback():
    """String ranges for edge cases slice syntax can't handle"""
    highlights = Dict()
    highlights["1,3,5,7,9"] = "odd-positions"  # Discrete positions
    highlights["10:20,30:40"] = "multi-segment"  # Multiple segments

    assert highlights[1] == "odd-positions"
    assert highlights[15] == "multi-segment"
    assert highlights[35] == "multi-segment"


def test_negative_positions_fail():
    """Negative positions should raise errors (ranges don't support)"""
    highlights = Dict()
    with pytest.raises(ValueError):
        highlights[-10:10] = "invalid"


def test_infinite_ranges():
    """Should handle infinite ranges"""
    highlights = Dict()
    highlights[1000:] = "tail-highlight"  # From position to end

    assert highlights[1000] == "tail-highlight"
    assert highlights[999999] == "tail-highlight"

    # But should still be efficient storage
    assert len(highlights) == 1


def test_dict_interface_compatibility():
    """Should work like a regular dict where possible"""
    highlights = Dict()
    highlights[100:200] = "highlight"
    highlights[300:400] = "selection"

    # Basic dict interface
    assert len(highlights) == 2

    # Iteration over segments (not individual positions)
    keys = list(highlights.keys())
    values = list(highlights.values())
    items = list(highlights.items())

    assert len(keys) == len(values) == len(items) == 2
    assert "highlight" in values
    assert "selection" in values


def test_range_queries():
    """Query ranges that span gaps should raise KeyError"""
    highlights = Dict()
    highlights[100:200] = "A"
    highlights[300:400] = "B"
    highlights[500:600] = "C"

    # Query a range that spans gaps should raise KeyError
    with pytest.raises(KeyError):
        highlights[150:550]  # Spans A, gap, B, gap, partial C


def test_stepped_ranges_not_supported():
    """Stepped slice syntax should raise clear errors"""
    highlights = Dict()
    with pytest.raises(ValueError, match="Stepped ranges not supported"):
        highlights[0:100:2] = "every-other"
