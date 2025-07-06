from arranges import Ranges


def test_subtraction_with_non_ranges_object():
    """Test subtraction operator with non-Ranges objects to cover line 281"""
    # When subtracting a string, it should convert to Ranges
    result = Ranges("1:10") - "3:7"
    assert result == Ranges("1:3,7:10")

    # When subtracting an integer (creates range :5)
    result = Ranges("1:10") - 5
    assert result == Ranges("5:10")

    # When subtracting a list
    result = Ranges("1:10") - [3, 4, 5]
    assert result == Ranges("1:3,6:10")

    # When subtracting a range object
    result = Ranges("1:10") - range(3, 7)
    assert result == Ranges("1:3,7:10")


def test_subtraction_edge_cases():
    """Test various edge cases for subtraction"""
    # Subtracting overlapping ranges
    assert Ranges("1:5,7:10") - "2:8" == Ranges("1:2,8:10")

    # Subtracting non-overlapping range
    assert Ranges("1:5") - "6:10" == Ranges("1:5")

    # Subtracting from empty range
    assert Ranges("") - "1:10" == Ranges("")

    # Subtracting larger range
    assert Ranges("3:7") - "1:10" == Ranges("")
