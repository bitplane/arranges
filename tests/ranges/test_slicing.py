from arranges import Ranges


def test_slice_infinite_range():
    """Test slicing an infinite range"""
    r = Ranges("1:")  # 1 to infinity
    assert r[:10] == Ranges("1:10")
    assert r[5:15] == Ranges("5:15")
    assert r[20:] == Ranges("20:")


def test_slice_finite_range():
    """Test slicing a finite range"""
    r = Ranges("0:100")
    assert r[:50] == Ranges("0:50")
    assert r[25:75] == Ranges("25:75")
    assert r[50:] == Ranges("50:100")
    assert r[150:200] == Ranges("")  # Outside range


def test_slice_multiple_segments():
    """Test slicing ranges with multiple segments"""
    r = Ranges("0:10,20:30,40:50")
    assert r[:25] == Ranges("0:10,20:25")
    assert r[5:45] == Ranges("5:10,20:30,40:45")
    assert r[25:] == Ranges("25:30,40:50")


def test_index_with_integer():
    """Test indexing ranges with integer (intlike) keys"""
    r = Ranges("0:10,20:30,40:50")

    # Integer in the ranges should return the integer itself
    assert r[5] == 5  # 5 is in 0:10
    assert r[25] == 25  # 25 is in 20:30
    assert r[45] == 45  # 45 is in 40:50

    # Integer not in ranges creates Ranges(key) & self intersection
    assert r[15] == Ranges("0:10")  # Ranges(15) = ":15", intersects with "0:10"
    assert r[35] == Ranges(
        "0:10,20:30"
    )  # Ranges(35) = ":35", intersects with "0:10,20:30"
