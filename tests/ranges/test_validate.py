from arranges import Ranges


def test_validate_class_method():
    """Test the validate class method to cover lines 312-315"""
    # When value is already a Ranges instance, return it directly
    ranges_obj = Ranges("1:10")
    validated = Ranges.validate(ranges_obj)
    assert validated is ranges_obj  # Should be the same object

    # When value is not a Ranges instance, create a new one
    validated = Ranges.validate("5:15")
    assert isinstance(validated, Ranges)
    assert validated == Ranges("5:15")

    # Test with various input types
    assert Ranges.validate(5) == Ranges(":5")  # Integer 5 creates range :5
    assert Ranges.validate([1, 2, 3]) == Ranges([1, 2, 3])
    assert Ranges.validate(range(5, 10)) == Ranges(range(5, 10))
    assert Ranges.validate(":10") == Ranges(":10")
    assert Ranges.validate("") == Ranges("")

    # Test with None
    assert Ranges.validate(None) == Ranges("")
